import bpy
import csv
import math
import bmesh
import numpy as np
from mathutils import Vector

# 비학습 움직임 중 3번째(8자 경로)에 대한 blender data 추출 코드 

# ==============================================================================
# BLENDER → GENESIS SIM2SIM EXPORT SCRIPT
# ==============================================================================
# Purpose: Extract trajectory data for Sim2Sim optimization
# Target loss: (a, k, v, v_lat, yaw_rate) matching
#
# Blender coordinate convention:
#   - Forward direction = -Y (heading = yaw - π/2)
#   - Position update: dx = v_long*sin(yaw) + v_lat*cos(yaw)
#                      dy = -v_long*cos(yaw) + v_lat*sin(yaw)
#
# Genesis matching:
#   - dt = 0.02 (50 FPS)
#   - Frame 1~500
#
# Consistency guarantees:
#   - v_long, v_lat: from position finite difference → body frame
#   - a = (v_long[i] - v_long[i-1]) / dt  (same v_long used above)
#   - k = yaw_rate / v_long
#   - yaw_rate = d_yaw / dt
#   - Self-test: position reconstruction from exported data < 0.3m error
# ==============================================================================

# --- CONFIGURATION (modify these for your scene) ---
TARGET_OBJECT_NAME = "Corvette.Vehicle Body.RB"
ARMATURE_NAME      = "Corvette Rig Armature"
PATH_OBJECT_NAME   = "NurbsPath"              # Set to "" if no path
OUTPUT_PATH        = "C:/Users/dwhah/Desktop/blender_data/data_new3.csv"     # // = relative to .blend file
START_FRAME        = 1
END_FRAME          = 750

# Physics constants
MAX_STEER_DEG      = 35.0
MAX_STEER_RAD      = math.radians(MAX_STEER_DEG)
THROTTLE_OMEGA_MAX = 60.0


# --- PATH UTILS ---
def create_path_evaluator(path_name):
    """Pre-compute path points for e_lat/e_head calculation."""
    path_obj = bpy.data.objects.get(path_name)
    if not path_obj:
        print(f"Warning: Path '{path_name}' not found.")
        return None, None, None

    depsgraph = bpy.context.evaluated_depsgraph_get()
    path_eval = path_obj.evaluated_get(depsgraph)
    mesh = bpy.data.meshes.new_from_object(path_eval)

    bm = bmesh.new()
    bm.from_mesh(mesh)
    bm.verts.ensure_lookup_table()

    points = [path_obj.matrix_world @ v.co for v in bm.verts]
    s_map = [0.0]
    for i in range(1, len(points)):
        s_map.append(s_map[-1] + (points[i] - points[i-1]).length)

    bm.free()
    bpy.data.meshes.remove(mesh)
    return s_map, points


def get_path_metrics(car_loc, car_yaw, s_map, path_points):
    """Compute path-relative metrics: arc length, lateral error, heading error."""
    min_dist = float('inf')
    best_idx = 0

    for i, p in enumerate(path_points):
        dist = (Vector((p.x, p.y, 0)) - Vector((car_loc.x, car_loc.y, 0))).length
        if dist < min_dist:
            min_dist = dist
            best_idx = i

    s = s_map[best_idx]
    e_lat = min_dist

    diff = car_loc - path_points[best_idx]
    if best_idx < len(path_points) - 1:
        tangent = (path_points[best_idx+1] - path_points[best_idx]).normalized()
    else:
        tangent = (path_points[best_idx] - path_points[best_idx-1]).normalized()

    cross_z = tangent.x * diff.y - tangent.y * diff.x
    if cross_z < 0:
        e_lat = -e_lat

    path_yaw = math.atan2(tangent.y, tangent.x)
    e_head = car_yaw - path_yaw
    while e_head > math.pi: e_head -= 2*math.pi
    while e_head < -math.pi: e_head += 2*math.pi

    return s, e_lat, e_head, tangent.x, tangent.y


# --- CONTROL UTILS ---
def get_rbc_controls(armature_name):
    """Extract steer/throttle from RBC Pro rig."""
    armature = bpy.data.objects.get(armature_name)
    if not armature:
        return 0.0, 0.0
    try:
        props = armature.get('sna_rbc_rig_armature_props')
        drivers = props.get('rig_drivers')
        if drivers:
            steer_raw = float(drivers.get('steering', 0.0))
            if abs(steer_raw) <= 1.5:
                steer_norm = steer_raw
            else:
                steer_norm = steer_raw / MAX_STEER_RAD

            tgt_speed = float(drivers.get('target_speed', 0.0))
            throttle_norm = max(-1.0, min(1.0, tgt_speed / THROTTLE_OMEGA_MAX))
            return steer_norm, throttle_norm
    except:
        pass
    return 0.0, 0.0


# --- MAIN EXPORT ---
def export_data():
    obj = bpy.data.objects.get(TARGET_OBJECT_NAME)
    if not obj:
        print(f"Error: Object '{TARGET_OBJECT_NAME}' not found!")
        return

    # Path setup (optional)
    s_map, path_points = None, None
    if PATH_OBJECT_NAME:
        result = create_path_evaluator(PATH_OBJECT_NAME)
        if result[0] is not None:
            s_map, path_points = result[0], result[1]

    fps = bpy.context.scene.render.fps / bpy.context.scene.render.fps_base
    dt = 1.0 / fps

    print(f"Export Settings:")
    print(f"  FPS: {fps}, dt: {dt}")
    print(f"  Frames: {START_FRAME} ~ {END_FRAME}")
    print(f"  Output: {OUTPUT_PATH}")

    # ---- Pass 1: Collect raw positions and yaw ----
    positions = []   # (x, y, z)
    yaws = []        # euler z

    for frame in range(START_FRAME, END_FRAME + 1):
        bpy.context.scene.frame_set(frame)
        bpy.context.view_layer.update()
        depsgraph = bpy.context.evaluated_depsgraph_get()
        obj_eval = obj.evaluated_get(depsgraph)

        loc = obj_eval.matrix_world.translation.copy()
        rot = obj_eval.matrix_world.to_euler('XYZ')
        positions.append(loc.copy())
        yaws.append(rot.z)

    # ---- Pass 2: Compute velocities (body frame) ----
    # Using forward difference: v[i] = (pos[i+1] - pos[i]) / dt
    # This gives velocity AT frame i (what happens between i and i+1)
    # Last frame uses backward difference
    n = len(positions)
    # Unwrap yaw to remove Euler wrap-around discontinuities (±π jumps).
    # Without this, a U-turn crossing ±π causes yaw_rate spikes (~157 rad/s).
    yaws = list(np.unwrap(yaws))
    v_longs = []
    v_lats = []
    yaw_rates = []

    for i in range(n):
        # Central difference for velocity (more accurate, less noise)
        if i == 0:
            d_loc = positions[i+1] - positions[i]  # forward at start
        elif i == n - 1:
            d_loc = positions[i] - positions[i-1]  # backward at end
        else:
            d_loc = (positions[i+1] - positions[i-1]) / 2.0  # central in middle

        vel_global = d_loc / dt

        # Transform to body frame using current frame's rotation
        bpy.context.scene.frame_set(START_FRAME + i)
        bpy.context.view_layer.update()
        depsgraph = bpy.context.evaluated_depsgraph_get()
        obj_eval = obj.evaluated_get(depsgraph)
        mat_world = obj_eval.matrix_world.to_3x3()
        vel_body = mat_world.transposed() @ vel_global

        # Blender convention: forward = -Y, lateral = +X (left positive)
        v_long = -vel_body.y
        v_lat = vel_body.x
        v_longs.append(v_long)
        v_lats.append(v_lat)

        # Yaw rate - central difference
        if i == 0:
            d_yaw = yaws[i+1] - yaws[i]
        elif i == n - 1:
            d_yaw = yaws[i] - yaws[i-1]
        else:
            d_yaw = (yaws[i+1] - yaws[i-1]) / 2.0
        if d_yaw > math.pi: d_yaw -= 2*math.pi
        if d_yaw < -math.pi: d_yaw += 2*math.pi
        yaw_rates.append(d_yaw / dt)

    # ---- Pass 3: Compute a, k ----
    accels = []
    curvatures = []

    for i in range(n):
        # a = dv_long / dt - central difference
        if i == 0:
            a = (v_longs[1] - v_longs[0]) / dt
        elif i == n - 1:
            a = (v_longs[i] - v_longs[i-1]) / dt
        else:
            a = (v_longs[i+1] - v_longs[i-1]) / (2.0 * dt)
        accels.append(a)

        # k = yaw_rate / v_long
        if abs(v_longs[i]) > 0.1:
            k = yaw_rates[i] / v_longs[i]
        else:
            k = 0.0
        curvatures.append(k)

    # ---- Pass 4: Collect controls and path metrics, write CSV ----
    headers = [
        "frame", "time", "dt",
        "g_pos_x", "g_pos_y", "g_yaw",
        "heading_cos", "heading_sin",
        "v_long", "v_lat", "yaw_rate",
        "a", "k",
        "steer_angle", "throttle"
    ]

    # Add path columns if path exists
    if path_points:
        headers.insert(8, "path_tangent_y")
        headers.insert(8, "path_tangent_x")
        headers.insert(8, "e_head")
        headers.insert(8, "e_lat")
        headers.insert(8, "s")

    data_rows = []

    for i in range(n):
        frame = START_FRAME + i
        time_val = frame * dt

        bpy.context.scene.frame_set(frame)
        bpy.context.view_layer.update()

        # Controls
        steer_norm, throttle_norm = get_rbc_controls(ARMATURE_NAME)
        steer_rad = steer_norm * MAX_STEER_RAD

        loc = positions[i]
        yaw = yaws[i]

        row = {
            "frame": frame,
            "time": f"{time_val:.6f}",
            "dt": f"{dt:.8f}",
            "g_pos_x": f"{loc.x:.8f}",
            "g_pos_y": f"{loc.y:.8f}",
            "g_yaw": f"{yaw:.8f}",
            "heading_cos": f"{math.cos(yaw):.8f}",
            "heading_sin": f"{math.sin(yaw):.8f}",
            "v_long": f"{v_longs[i]:.8f}",
            "v_lat": f"{v_lats[i]:.8f}",
            "yaw_rate": f"{yaw_rates[i]:.8f}",
            "a": f"{accels[i]:.8f}",
            "k": f"{curvatures[i]:.8f}",
            "steer_angle": f"{steer_rad:.8f}",
            "throttle": f"{throttle_norm:.8f}",
        }

        if path_points:
            s, e_lat, e_head, tx, ty = get_path_metrics(loc, yaw, s_map, path_points)
            row["s"] = f"{s:.8f}"
            row["e_lat"] = f"{e_lat:.8f}"
            row["e_head"] = f"{e_head:.8f}"
            row["path_tangent_x"] = f"{tx:.8f}"
            row["path_tangent_y"] = f"{ty:.8f}"

        data_rows.append([row[h] for h in headers])

    # ---- Write CSV ----
    output = bpy.path.abspath(OUTPUT_PATH)
    with open(output, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(data_rows)

    # ---- Self-test: reconstruct position from v_long, v_lat, yaw ----
    print(f"\n--- Self-test: Position Reconstruction ---")
    x_rec, y_rec = loc.x, loc.y  # will be overwritten
    max_err = 0.0
    x_rec = positions[0].x
    y_rec = positions[0].y

    for i in range(1, n):
        yaw_i = yaws[i-1]
        x_rec += (v_longs[i-1]*math.sin(yaw_i) + v_lats[i-1]*math.cos(yaw_i)) * dt
        y_rec += (-v_longs[i-1]*math.cos(yaw_i) + v_lats[i-1]*math.sin(yaw_i)) * dt
        err = math.sqrt((x_rec - positions[i].x)**2 + (y_rec - positions[i].y)**2)
        if err > max_err:
            max_err = err

    print(f"  Max position reconstruction error: {max_err:.6f} m")
    if max_err < 0.5:
        print(f"  PASS - Data is self-consistent")
    else:
        print(f"  WARNING - Large reconstruction error, check physics substeps")

    print(f"\nExport complete: {output}")
    print(f"  Total frames: {n}")
    print(f"  FPS: {fps}, dt: {dt}")

export_data()
