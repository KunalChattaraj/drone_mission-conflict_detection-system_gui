import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D
import random
from datetime import datetime, timedelta
import threading
import time
import os

class DroneMission:
    def __init__(self, mission_id, waypoints, start_time, duration, status="active", status_timestamp=None):
        self.mission_id = mission_id
        self.waypoints = waypoints  # List of (x, y, z, t)
        self.start_time = start_time
        self.duration = duration
        self.status = status  # "active", "aborted", "inactive", "completed"
        self.status_timestamp = status_timestamp or datetime.now()
        self.conflict = False

class DroneConflictDetectionSystem:
    def __init__(self):
        self.simulated_missions = []
        self.primary_mission = None
        self.airspace_data = []  # This should only contain active missions from simulated_missions
        self.conflicted_missions = []
        self.simulated_missions_file = "simulated_missions.csv"
        self.airspace_data_file = "airspace_data.csv"
        
    def reset_all_data(self):
        """Reset all data and delete CSV files"""
        self.simulated_missions = []
        self.primary_mission = None
        self.airspace_data = []
        self.conflicted_missions = []
        
        # Delete CSV files if they exist
        try:
            if os.path.exists(self.simulated_missions_file):
                os.remove(self.simulated_missions_file)
            if os.path.exists(self.airspace_data_file):
                os.remove(self.airspace_data_file)
            if os.path.exists("primary_mission.csv"):
                os.remove("primary_mission.csv")
            if os.path.exists("high_conflict_primary.csv"):
                os.remove("high_conflict_primary.csv")
            print("All data reset and CSV files deleted")
        except Exception as e:
            print(f"Error deleting files: {e}")
        
    def generate_simulated_missions(self, num_missions=1000, save_to_csv=True):
        """Generate 1000 simulated drone missions"""
        missions = []
        
        for i in range(num_missions):
            mission_id = f"SIM_{i+1:04d}"
            start_time = datetime.now() + timedelta(hours=random.randint(0, 24))
            duration = timedelta(minutes=random.randint(30, 180))
            
            # Generate random waypoints
            num_waypoints = random.randint(3, 8)
            waypoints = []
            
            start_x = random.uniform(-1000, 1000)
            start_y = random.uniform(-1000, 1000)
            start_z = random.uniform(50, 500)
            
            for j in range(num_waypoints):
                x = start_x + random.uniform(-500, 500)
                y = start_y + random.uniform(-500, 500)
                z = max(50, start_z + random.uniform(-100, 100))
                t = start_time + timedelta(minutes=j * duration.total_seconds() / 60 / num_waypoints)
                waypoints.append((x, y, z, t))
            
            mission = DroneMission(mission_id, waypoints, start_time, duration, "active")
            missions.append(mission)
        
        self.simulated_missions = missions
        # Airspace data should only contain active missions from simulated_missions
        self.airspace_data = [m for m in self.simulated_missions if m.status == "active"]
        
        if save_to_csv:
            # Save to simulated_missions.csv
            self.save_missions_to_csv(self.simulated_missions, self.simulated_missions_file)
            # Save active missions to airspace_data.csv
            self.save_missions_to_csv(self.airspace_data, self.airspace_data_file)
        
        return missions

    def generate_high_conflict_test_case(self):
        """Generate a primary mission that conflicts with multiple simulated missions"""
        # First, ensure we have the base simulated missions
        if len(self.simulated_missions) < 50:
            self.generate_simulated_missions(1000)
        
        # Create a primary mission that passes through many existing mission paths
        primary_id = "HIGH_CONFLICT_PRIMARY"
        start_time = datetime.now() + timedelta(hours=2)
        duration = timedelta(minutes=120)
        
        # Create waypoints that intentionally conflict with many missions
        waypoints = []
        
        # Get active missions to create conflicts with
        active_missions = [m for m in self.simulated_missions if m.status == "active"]
        conflict_missions = random.sample(active_missions, min(30, len(active_missions)))
        
        for i, mission in enumerate(conflict_missions):
            if i >= 30:  # Limit to 30 conflicts for testing
                break
            # Take a waypoint from the conflicting mission and adjust slightly
            conflict_wp = random.choice(mission.waypoints)
            x, y, z, t = conflict_wp
            # Create a point very close to cause conflict (within 50m)
            waypoints.append((
                x + random.uniform(-40, 40),
                y + random.uniform(-40, 40), 
                z + random.uniform(-20, 20),
                t + timedelta(seconds=random.randint(-45, 45))
            ))
        
        # Add a few more random waypoints
        for _ in range(3):
            waypoints.append((
                random.uniform(-1000, 1000),
                random.uniform(-1000, 1000),
                random.uniform(50, 500),
                start_time + timedelta(minutes=random.randint(10, 110))
            ))
        
        # Sort waypoints by time
        waypoints.sort(key=lambda wp: wp[3])
        
        self.primary_mission = DroneMission(primary_id, waypoints, start_time, duration, "pending")
        self.save_missions_to_csv([self.primary_mission], "high_conflict_primary.csv")
        
        return self.primary_mission
    
    def generate_primary_mission(self, save_to_csv=True):
        """Generate a normal primary mission for testing"""
        mission_id = "PRIMARY_" + datetime.now().strftime("%Y%m%d_%H%M%S")
        start_time = datetime.now() + timedelta(hours=2)
        duration = timedelta(minutes=90)
        
        # Generate waypoints in safe areas
        waypoints = [
            (-800, 800, 100, start_time),
            (-600, 600, 150, start_time + timedelta(minutes=30)),
            (-400, 400, 200, start_time + timedelta(minutes=60)),
            (-200, 200, 180, start_time + timedelta(minutes=90))
        ]
        
        self.primary_mission = DroneMission(mission_id, waypoints, start_time, duration, "pending")
        
        if save_to_csv:
            self.save_missions_to_csv([self.primary_mission], "primary_mission.csv")
        
        return self.primary_mission
    
    def save_missions_to_csv(self, missions, filename):
        """Save missions to CSV file with status information"""
        data = []
        for mission in missions:
            for i, (x, y, z, t) in enumerate(mission.waypoints):
                data.append({
                    'mission_id': mission.mission_id,
                    'waypoint_id': i+1,
                    'x': x,
                    'y': y,
                    'z': z,
                    'timestamp': t,
                    'start_time': mission.start_time,
                    'duration_minutes': mission.duration.total_seconds() / 60,
                    'status': mission.status,
                    'status_timestamp': mission.status_timestamp
                })
        
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        print(f"Missions saved to {filename}")
    
    def load_missions_from_csv(self, filename):
        """Load missions from CSV file with status information"""
        try:
            df = pd.read_csv(filename)
            missions = []
            
            for mission_id in df['mission_id'].unique():
                mission_data = df[df['mission_id'] == mission_id]
                waypoints = []
                
                for _, row in mission_data.iterrows():
                    waypoints.append((
                        row['x'], row['y'], row['z'], 
                        pd.to_datetime(row['timestamp'])
                    ))
                
                start_time = pd.to_datetime(mission_data['start_time'].iloc[0])
                duration = timedelta(minutes=mission_data['duration_minutes'].iloc[0])
                status = mission_data['status'].iloc[0]
                status_timestamp = pd.to_datetime(mission_data['status_timestamp'].iloc[0])
                
                mission = DroneMission(mission_id, waypoints, start_time, duration, status, status_timestamp)
                missions.append(mission)
            
            return missions
        except Exception as e:
            print(f"Error loading missions: {e}")
            return []
    
    def update_simulated_missions_csv(self):
        """Update the simulated missions CSV file with current status"""
        self.save_missions_to_csv(self.simulated_missions, self.simulated_missions_file)
        print("Simulated missions CSV updated with current status")
    
    def update_airspace_data_csv(self):
        """Update the airspace data CSV file with only active missions from simulated_missions"""
        active_missions = [m for m in self.simulated_missions if m.status == "active"]
        self.airspace_data = active_missions  # Keep airspace_data in sync
        self.save_missions_to_csv(active_missions, self.airspace_data_file)
        print("Airspace data CSV updated with active missions only")
    
    def check_conflicts(self, primary_mission, test_missions, safety_distance=100, time_threshold=60):
        """Check for conflicts between primary mission and test missions"""
        conflicted_missions = []
        
        for test_mission in test_missions:
            if test_mission.status == "aborted" or test_mission.status == "inactive":
                continue
                
            conflict_found = False
            
            # Simple conflict detection based on spatio-temporal proximity
            for primary_wp in primary_mission.waypoints:
                px, py, pz, pt = primary_wp
                
                for test_wp in test_mission.waypoints:
                    tx, ty, tz, tt = test_wp
                    
                    # Check time proximity
                    time_diff = abs((pt - tt).total_seconds())
                    
                    if time_diff <= time_threshold:
                        # Check spatial proximity
                        distance = np.sqrt((px - tx)**2 + (py - ty)**2 + (pz - tz)**2)
                        
                        if distance <= safety_distance:
                            conflict_found = True
                            print(f"CONFLICT: {test_mission.mission_id} - Distance: {distance:.2f}m, Time diff: {time_diff:.2f}s")
                            break
                
                if conflict_found:
                    break
            
            if conflict_found:
                test_mission.conflict = True
                conflicted_missions.append(test_mission)
        
        self.conflicted_missions = conflicted_missions
        return conflicted_missions
    
    def abort_mission(self, mission_id):
        """Abort a specific mission and update CSVs"""
        mission_found = False
        
        # Update status in simulated_missions
        for mission in self.simulated_missions:
            if mission.mission_id == mission_id:
                mission.status = "aborted"
                mission.status_timestamp = datetime.now()
                mission.conflict = False
                mission_found = True
                print(f"Mission {mission_id} aborted at {mission.status_timestamp}")
                break
        
        if mission_found:
            # Update both CSV files
            self.update_simulated_missions_csv()
            self.update_airspace_data_csv()  # This will remove aborted missions from airspace
            return True
        return False
    
    def abort_multiple_missions(self, mission_ids):
        """Abort multiple missions at once"""
        aborted_count = 0
        for mission_id in mission_ids:
            if self.abort_mission(mission_id):
                aborted_count += 1
        return aborted_count
    
    def abort_all_conflicted_missions(self):
        """Abort all currently conflicted missions"""
        aborted_count = 0
        for mission in self.conflicted_missions:
            if self.abort_mission(mission.mission_id):
                aborted_count += 1
        
        # Clear the conflicted missions list after aborting
        self.conflicted_missions = []
        print(f"All {aborted_count} conflicted missions aborted")
        return aborted_count
    
    def accept_primary_mission(self):
        """Accept primary mission and update both CSV files"""
        if self.primary_mission and len(self.conflicted_missions) == 0:
            # Set primary mission as active
            self.primary_mission.status = "active"
            self.primary_mission.status_timestamp = datetime.now()
            
            # Add to simulated_missions
            self.simulated_missions.append(self.primary_mission)
            
            # Update both CSV files
            self.update_simulated_missions_csv()
            self.update_airspace_data_csv()  # This will include the new primary mission
            
            return True
        return False
    
    def reject_primary_mission(self):
        """Reject primary mission - add to simulated_missions as inactive"""
        if self.primary_mission:
            self.primary_mission.status = "inactive"
            self.primary_mission.status_timestamp = datetime.now()
            
            # Add to simulated_missions only (not to airspace)
            self.simulated_missions.append(self.primary_mission)
            
            # Update only simulated_missions CSV
            self.update_simulated_missions_csv()
            
            return True
        return False
    
    def get_mission_statistics(self):
        """Get detailed statistics about missions"""
        total_simulated = len(self.simulated_missions)
        active_missions = len([m for m in self.simulated_missions if m.status == "active"])
        aborted_missions = len([m for m in self.simulated_missions if m.status == "aborted"])
        inactive_missions = len([m for m in self.simulated_missions if m.status == "inactive"])
        completed_missions = len([m for m in self.simulated_missions if m.status == "completed"])
        
        # Airspace missions should be the same as active missions in simulated_missions
        airspace_missions = len(self.airspace_data)
        
        return {
            'total_simulated': total_simulated,
            'active_missions': active_missions,
            'aborted_missions': aborted_missions,
            'inactive_missions': inactive_missions,
            'completed_missions': completed_missions,
            'airspace_missions': airspace_missions,
            'current_conflicts': len(self.conflicted_missions),
            'primary_mission': self.primary_mission.mission_id if self.primary_mission else None
        }

class VisualizationWindow:
    def __init__(self, parent, dcs_system):
        self.parent = parent
        self.dcs = dcs_system
        self.setup_visualization_window()
    
    def setup_visualization_window(self):
        """Create visualization window with 3D plot"""
        self.viz_window = tk.Toplevel(self.parent)
        self.viz_window.title("Drone Mission Visualization - 3D Airspace")
        self.viz_window.geometry("1200x900")
        
        # Create main frame
        main_frame = ttk.Frame(self.viz_window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Visualization controls
        controls_frame = ttk.LabelFrame(main_frame, text="Visualization Controls", padding="10")
        controls_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(controls_frame, text="Show Primary Mission", 
                  command=lambda: self.plot_mission_focus("primary")).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls_frame, text="Show Conflict Scenario", 
                  command=lambda: self.plot_mission_focus("conflict")).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls_frame, text="Show All Active Missions", 
                  command=lambda: self.plot_mission_focus("all")).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls_frame, text="Close", 
                  command=self.viz_window.destroy).pack(side=tk.RIGHT, padx=5)
        
        # Info frame
        info_frame = ttk.LabelFrame(main_frame, text="Visualization Info", padding="5")
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        info_text = tk.Text(info_frame, height=3, width=100)
        info_text.pack(fill=tk.X)
        info_text.insert(tk.END, 
                        "Primary Mission: RED solid line | Active Missions: BLUE solid lines | "
                        "Conflicted Missions: ORANGE dashed lines | Conflict Points: RED X markers")
        info_text.config(state=tk.DISABLED)
        
        # Create matplotlib figure
        self.fig = plt.Figure(figsize=(12, 8), dpi=100)
        self.ax = self.fig.add_subplot(111, projection='3d')
        
        # Embed the figure in tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, main_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Show initial plot
        self.plot_mission_focus("primary")
    
    def plot_mission_focus(self, focus_type):
        """Plot missions based on focus type"""
        self.ax.clear()
        
        if focus_type == "primary":
            self._plot_primary_mission_with_nearby()
        elif focus_type == "conflict":
            self._plot_conflict_scenario()
        elif focus_type == "all":
            self._plot_all_active_missions()
        else:
            self.ax.text2D(0.5, 0.5, "No data available for visualization", 
                          transform=self.ax.transAxes, ha='center', fontsize=12)
        
        self.ax.set_xlabel('X Coordinate (m)')
        self.ax.set_ylabel('Y Coordinate (m)')
        self.ax.set_zlabel('Altitude (m)')
        self.ax.set_title(f'Drone Mission Visualization - {focus_type.capitalize()} Focus', fontsize=14)
        
        # Add grid for better visualization
        self.ax.grid(True, alpha=0.3)
        
        self.canvas.draw()
    
    def _plot_primary_mission_with_nearby(self):
        """Plot primary mission and nearby missions"""
        if not self.dcs.primary_mission:
            self.ax.text2D(0.5, 0.5, "No primary mission available", 
                          transform=self.ax.transAxes, ha='center', fontsize=12)
            return
        
        # Plot primary mission
        primary_waypoints = np.array([(wp[0], wp[1], wp[2]) for wp in self.dcs.primary_mission.waypoints])
        if len(primary_waypoints) > 0:
            self.ax.plot(primary_waypoints[:, 0], primary_waypoints[:, 1], primary_waypoints[:, 2], 
                        'ro-', linewidth=4, markersize=10, label='Primary Mission', alpha=0.8)
            
            # Plot primary waypoints as larger points
            self.ax.scatter(primary_waypoints[:, 0], primary_waypoints[:, 1], primary_waypoints[:, 2], 
                          c='red', s=100, alpha=0.8)
        
        # Find and plot nearby missions (within 500m of any primary waypoint)
        nearby_missions = []
        for mission in self.dcs.simulated_missions:
            if mission.status == "active":
                for wp_primary in self.dcs.primary_mission.waypoints:
                    for wp_mission in mission.waypoints:
                        distance = np.sqrt((wp_primary[0]-wp_mission[0])**2 + 
                                         (wp_primary[1]-wp_mission[1])**2 + 
                                         (wp_primary[2]-wp_mission[2])**2)
                        if distance < 500:  # Within 500m
                            nearby_missions.append(mission)
                            break
                    else:
                        continue
                    break
        
        # Plot nearby missions
        for i, mission in enumerate(nearby_missions[:15]):  # Limit to 15 for clarity
            waypoints = np.array([(wp[0], wp[1], wp[2]) for wp in mission.waypoints])
            if len(waypoints) > 0:
                self.ax.plot(waypoints[:, 0], waypoints[:, 1], waypoints[:, 2], 
                            'b-', alpha=0.6, linewidth=2, markersize=6, 
                            label=f'Nearby Mission {i+1}' if i < 5 else "")
                
                # Plot mission waypoints
                self.ax.scatter(waypoints[:, 0], waypoints[:, 1], waypoints[:, 2], 
                              c='blue', s=30, alpha=0.6)
        
        if len(primary_waypoints) > 0 or nearby_missions:
            self.ax.legend()
    
    def _plot_conflict_scenario(self):
        """Plot primary mission and conflicted missions"""
        if not self.dcs.primary_mission:
            self.ax.text2D(0.5, 0.5, "No primary mission available", 
                          transform=self.ax.transAxes, ha='center', fontsize=12)
            return
        
        # Plot primary mission
        primary_waypoints = np.array([(wp[0], wp[1], wp[2]) for wp in self.dcs.primary_mission.waypoints])
        if len(primary_waypoints) > 0:
            self.ax.plot(primary_waypoints[:, 0], primary_waypoints[:, 1], primary_waypoints[:, 2], 
                        'ro-', linewidth=4, markersize=10, label='Primary Mission', alpha=0.8)
        
        if not self.dcs.conflicted_missions:
            self.ax.text2D(0.5, 0.4, "No conflicts detected", 
                          transform=self.ax.transAxes, ha='center', fontsize=12)
            return
        
        # Plot conflicted missions
        conflict_points = []
        for i, mission in enumerate(self.dcs.conflicted_missions):
            waypoints = np.array([(wp[0], wp[1], wp[2]) for wp in mission.waypoints])
            if len(waypoints) > 0:
                color = 'orange' if mission.status == "active" else 'red'
                linestyle = '--' if mission.status == "active" else ':'
                
                self.ax.plot(waypoints[:, 0], waypoints[:, 1], waypoints[:, 2], 
                            color=color, linestyle=linestyle, linewidth=3, markersize=8,
                            label=f'Conflict {i+1}' if i < 5 else "")
                
                # Find and mark conflict points
                for primary_wp in self.dcs.primary_mission.waypoints:
                    for mission_wp in mission.waypoints:
                        distance = np.sqrt((primary_wp[0]-mission_wp[0])**2 + 
                                         (primary_wp[1]-mission_wp[1])**2 + 
                                         (primary_wp[2]-mission_wp[2])**2)
                        time_diff = abs((primary_wp[3] - mission_wp[3]).total_seconds())
                        if distance < 100 and time_diff < 60:  # Conflict criteria
                            conflict_points.append((mission_wp[0], mission_wp[1], mission_wp[2]))
        
        # Plot all conflict points
        if conflict_points:
            conflict_array = np.array(conflict_points)
            self.ax.scatter(conflict_array[:, 0], conflict_array[:, 1], conflict_array[:, 2], 
                          c='red', s=200, marker='X', alpha=0.8, label='Conflict Points')
        
        self.ax.legend()
    
    def _plot_all_active_missions(self):
        """Plot all active missions in airspace"""
        # Get all active missions (from simulated_missions and include primary if it exists)
        active_missions = [m for m in self.dcs.simulated_missions if m.status == "active"]
        
        # Include primary mission if it exists (even if pending)
        if self.dcs.primary_mission and self.dcs.primary_mission not in active_missions:
            active_missions.append(self.dcs.primary_mission)
        
        if not active_missions:
            self.ax.text2D(0.5, 0.5, "No active missions available", 
                          transform=self.ax.transAxes, ha='center', fontsize=12)
            return
        
        # Plot all active missions
        mission_count = 0
        for mission in active_missions[:25]:  # Limit to 25 for clarity
            waypoints = np.array([(wp[0], wp[1], wp[2]) for wp in mission.waypoints])
            if len(waypoints) > 0:
                # Different styling for primary vs regular missions
                if mission.mission_id.startswith('PRIMARY') or mission.mission_id.startswith('HIGH_CONFLICT'):
                    color = 'red'
                    linestyle = '-'
                    linewidth = 4
                    marker_size = 10
                    label = 'Primary Mission' if mission_count == 0 else ""
                else:
                    color = 'blue'
                    linestyle = '-'
                    linewidth = 1
                    marker_size = 5
                    label = f'Mission {mission_count+1}' if mission_count < 5 else ""
                
                self.ax.plot(waypoints[:, 0], waypoints[:, 1], waypoints[:, 2], 
                            color=color, linestyle=linestyle, linewidth=linewidth, 
                            alpha=0.7, label=label)
                
                # Plot waypoints
                self.ax.scatter(waypoints[:, 0], waypoints[:, 1], waypoints[:, 2], 
                              color=color, s=marker_size*10, alpha=0.7)
                
                mission_count += 1
        
        if mission_count > 0:
            self.ax.legend()

class DCSGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Drone Conflict Detection System - DCS AIRSPACE DATA")
        self.root.geometry("1200x800")
        
        self.dcs = DroneConflictDetectionSystem()
        
        # Load existing data if available
        self.load_existing_data()
        
        self.setup_gui()
        
    def load_existing_data(self):
        """Load existing mission data from CSV files if they exist"""
        try:
            if os.path.exists(self.dcs.simulated_missions_file):
                self.dcs.simulated_missions = self.dcs.load_missions_from_csv(self.dcs.simulated_missions_file)
                print(f"Loaded {len(self.dcs.simulated_missions)} existing simulated missions")
            
            if os.path.exists(self.dcs.airspace_data_file):
                airspace_missions = self.dcs.load_missions_from_csv(self.dcs.airspace_data_file)
                self.dcs.airspace_data = airspace_missions
                print(f"Loaded {len(self.dcs.airspace_data)} existing airspace missions")
                
                # Verify consistency
                active_in_simulated = len([m for m in self.dcs.simulated_missions if m.status == "active"])
                if len(self.dcs.airspace_data) != active_in_simulated:
                    print(f"Warning: Inconsistency detected. Active in simulated: {active_in_simulated}, in airspace: {len(self.dcs.airspace_data)}")
                    # Fix the inconsistency
                    self.dcs.update_airspace_data_csv()
        except Exception as e:
            print(f"Error loading existing data: {e}")
        
    def setup_gui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="DCS AIRSPACE DATA", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=4, pady=(0, 20))
        
        # Control buttons frame
        control_frame = ttk.LabelFrame(main_frame, text="Mission Control", padding="10")
        control_frame.grid(row=1, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Mission generation buttons - Row 1
        ttk.Button(control_frame, text="Generate 1000 Simulated Missions", 
                  command=self.generate_simulated_missions).grid(row=0, column=0, padx=5, pady=2)
        ttk.Button(control_frame, text="Generate Primary Mission", 
                  command=self.generate_primary_mission).grid(row=0, column=1, padx=5, pady=2)
        ttk.Button(control_frame, text="Upload Primary Mission", 
                  command=self.upload_primary_mission).grid(row=0, column=2, padx=5, pady=2)
        ttk.Button(control_frame, text="Refresh Mission Data", 
                  command=self.refresh_data).grid(row=0, column=3, padx=5, pady=2)
        
        # Test case and utility buttons - Row 2
        ttk.Button(control_frame, text="Test Case: Multiple Conflicts", 
                  command=self.generate_high_conflict_test).grid(row=1, column=0, padx=5, pady=2)
        ttk.Button(control_frame, text="Reset All Data", 
                  command=self.reset_all_data).grid(row=1, column=1, padx=5, pady=2)
        ttk.Button(control_frame, text="Visualize Missions (3D)", 
                  command=self.visualize_missions).grid(row=1, column=2, padx=5, pady=2)
        
        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="System Status", padding="10")
        status_frame.grid(row=2, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.status_text = tk.Text(status_frame, height=2, width=100)
        self.status_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Conflict detection frame
        conflict_frame = ttk.LabelFrame(main_frame, text="Conflict Detection", padding="10")
        conflict_frame.grid(row=3, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(conflict_frame, text="Check Conflicts", 
                  command=self.check_conflicts).grid(row=0, column=0, padx=5)
        ttk.Button(conflict_frame, text="Re-check Conflicts", 
                  command=self.recheck_conflicts).grid(row=0, column=1, padx=5)
        ttk.Button(conflict_frame, text="Accept Mission", 
                  command=self.accept_mission).grid(row=0, column=2, padx=5)
        ttk.Button(conflict_frame, text="Reject Mission", 
                  command=self.reject_mission).grid(row=0, column=3, padx=5)
        ttk.Button(conflict_frame, text="Abort All Conflicts", 
                  command=self.abort_all_conflicts).grid(row=0, column=4, padx=5)
        
        # Results frame
        results_frame = ttk.LabelFrame(main_frame, text="Conflict Results", padding="10")
        results_frame.grid(row=4, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Treeview for conflicted missions
        columns = ("Mission ID", "Start Time", "Duration", "Status", "Last Status Update", "Action")
        self.conflict_tree = ttk.Treeview(results_frame, columns=columns, show="headings", height=5)
        
        for col in columns:
            self.conflict_tree.heading(col, text=col)
            if col in ["Mission ID", "Action"]:
                self.conflict_tree.column(col, width=120)
            else:
                self.conflict_tree.column(col, width=150)
        
        self.conflict_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.conflict_tree.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.conflict_tree.configure(yscrollcommand=scrollbar.set)
        
        # Abort buttons frame - Enhanced with better layout
        abort_frame = ttk.LabelFrame(results_frame, text="Mission Abort Controls", padding="10")
        abort_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # Create a frame for the abort buttons
        abort_buttons_frame = ttk.Frame(abort_frame)
        abort_buttons_frame.pack(fill=tk.X)
        
        ttk.Button(abort_buttons_frame, text="Abort Selected Mission(s)", 
                  command=self.abort_selected_mission, style="Accent.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(abort_buttons_frame, text="Abort All Conflicts", 
                  command=self.abort_all_conflicts, style="Accent.TButton").pack(side=tk.LEFT, padx=5)
        
        # Add selection info label
        self.selection_info = ttk.Label(abort_buttons_frame, text="Select missions from the table above to abort")
        self.selection_info.pack(side=tk.RIGHT, padx=5)
        
        # Bind selection event to update info
        self.conflict_tree.bind('<<TreeviewSelect>>', self.on_selection_change)
        
        # Statistics frame
        stats_frame = ttk.LabelFrame(main_frame, text="System Statistics", padding="2")
        stats_frame.grid(row=5, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(0, 2))
        
        self.stats_text = tk.Text(stats_frame, height=4, width=100)
        self.stats_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # Configure style for accent buttons
        style = ttk.Style()
        style.configure("Accent.TButton", background="#e74c3c", foreground="white")
        
        self.update_status("System initialized. Ready to generate missions.")
        self.update_stats()
    
    def on_selection_change(self, event):
        """Update selection info when missions are selected"""
        selected_items = self.conflict_tree.selection()
        if selected_items:
            count = len(selected_items)
            mission_ids = [self.conflict_tree.item(item)['values'][0] for item in selected_items[:3]]  # First 3 IDs
            if count > 3:
                self.selection_info.config(text=f"Selected {count} missions: {', '.join(mission_ids)}...")
            else:
                self.selection_info.config(text=f"Selected {count} missions: {', '.join(mission_ids)}")
        else:
            self.selection_info.config(text="Select missions from the table above to abort")
    
    def reset_all_data(self):
        """Reset all data and restart the system"""
        if messagebox.askyesno("Confirm Reset", 
                             "Are you sure you want to reset ALL data? This will delete all missions and CSV files."):
            self.dcs.reset_all_data()
            self.update_status("All data reset. System restarted.")
            self.conflict_tree.delete(*self.conflict_tree.get_children())
            self.update_stats()
    
    def visualize_missions(self):
        """Open visualization window"""
        if not self.dcs.simulated_missions and not self.dcs.primary_mission:
            messagebox.showwarning("Warning", "No mission data available for visualization. Please generate missions first.")
            return
        
        VisualizationWindow(self.root, self.dcs)
    
    def refresh_data(self):
        """Refresh mission data from CSV files"""
        self.load_existing_data()
        self.update_status("Mission data refreshed from CSV files")
        self.update_stats()
    
    def generate_simulated_missions(self):
        def generate():
            self.update_status("Generating 1000 simulated missions...")
            self.dcs.generate_simulated_missions(1000)
            self.update_status("1000 simulated missions generated! Both CSV files updated.")
            self.update_stats()
        
        threading.Thread(target=generate).start()
    
    def generate_high_conflict_test(self):
        """Generate primary mission with multiple conflicts"""
        if len(self.dcs.simulated_missions) < 50:
            messagebox.showwarning("Warning", "Need at least 50 simulated missions. Generating 1000 now...")
            self.generate_simulated_missions()
            return
            
        self.update_status("Generating high conflict test case (multiple conflicts)...")
        primary = self.dcs.generate_high_conflict_test_case()
        self.update_status(f"High conflict test case generated: {primary.mission_id}")
        self.update_stats()
        
        # Auto-check conflicts
        self.check_conflicts()
    
    def generate_primary_mission(self):
        self.update_status("Generating primary mission...")
        self.dcs.generate_primary_mission()
        self.update_status("Primary mission generated successfully!")
        self.update_stats()
    
    def upload_primary_mission(self):
        filename = filedialog.askopenfilename(title="Select Primary Mission CSV", 
                                            filetypes=[("CSV files", "*.csv")])
        if filename:
            missions = self.dcs.load_missions_from_csv(filename)
            if missions:
                self.dcs.primary_mission = missions[0]
                self.update_status(f"Primary mission loaded: {self.dcs.primary_mission.mission_id}")
                self.update_stats()
            else:
                messagebox.showerror("Error", "Failed to load primary mission from file.")
    
    def check_conflicts(self):
        if not self.dcs.primary_mission:
            messagebox.showwarning("Warning", "Please generate or upload a primary mission first.")
            return
        
        if not self.dcs.simulated_missions:
            messagebox.showwarning("Warning", "Please generate simulated missions first.")
            return
        
        def check():
            self.update_status("Checking for conflicts...")
            conflicted_missions = self.dcs.check_conflicts(
                self.dcs.primary_mission, 
                [m for m in self.dcs.simulated_missions if m.status == "active"]
            )
            
            self.update_conflict_tree(conflicted_missions)
            self.update_status(f"Conflict check completed. Found {len(conflicted_missions)} conflicts.")
            self.update_stats()
        
        threading.Thread(target=check).start()
    
    def recheck_conflicts(self):
        if not self.dcs.primary_mission:
            return
        
        def recheck():
            self.update_status("Re-checking conflicts...")
            conflicted_missions = self.dcs.check_conflicts(
                self.dcs.primary_mission, 
                [m for m in self.dcs.simulated_missions if m.status == "active"]
            )
            
            self.update_conflict_tree(conflicted_missions)
            self.update_status(f"Re-check completed. Found {len(conflicted_missions)} conflicts.")
            self.update_stats()
        
        threading.Thread(target=recheck).start()
    
    def abort_selected_mission(self):
        """Abort selected missions from the table (single or multiple)"""
        selected_items = self.conflict_tree.selection()
        if not selected_items:
            messagebox.showwarning("Warning", "Please select one or more missions to abort.")
            return
        
        mission_ids = [self.conflict_tree.item(item)['values'][0] for item in selected_items]
        
        if len(mission_ids) == 1:
            confirm_msg = f"Are you sure you want to abort mission {mission_ids[0]}?"
        else:
            confirm_msg = f"Are you sure you want to abort {len(mission_ids)} selected missions?"
        
        if messagebox.askyesno("Confirm Abort", confirm_msg):
            aborted_count = self.dcs.abort_multiple_missions(mission_ids)
            if aborted_count > 0:
                self.update_status(f"Aborted {aborted_count} selected missions. Both CSV files updated.")
                self.recheck_conflicts()
            else:
                messagebox.showerror("Error", "Failed to abort selected missions.")
    
    def abort_all_conflicts(self):
        """Abort all conflicted missions at once"""
        if not self.dcs.conflicted_missions:
            messagebox.showinfo("Info", "No conflicts to abort.")
            return
        
        if messagebox.askyesno("Confirm Abort All", 
                             f"Are you sure you want to abort all {len(self.dcs.conflicted_missions)} conflicted missions?"):
            aborted_count = self.dcs.abort_all_conflicted_missions()
            if aborted_count > 0:
                self.update_status(f"All {aborted_count} conflicted missions aborted. Both CSV files updated.")
                self.recheck_conflicts()
            else:
                messagebox.showerror("Error", "Failed to abort conflicted missions.")
    
    def accept_mission(self):
        if self.dcs.accept_primary_mission():
            self.update_status("Primary mission accepted and added to both CSV files.")
            self.dcs.primary_mission = None
            self.conflict_tree.delete(*self.conflict_tree.get_children())
            self.update_stats()
        else:
            messagebox.showwarning("Warning", 
                                 "Cannot accept mission. There are still conflicts or no primary mission.")
    
    def reject_mission(self):
        if self.dcs.reject_primary_mission():
            mission_id = self.dcs.primary_mission.mission_id if self.dcs.primary_mission else "Unknown"
            self.dcs.primary_mission = None
            self.conflict_tree.delete(*self.conflict_tree.get_children())
            self.update_status(f"Primary mission {mission_id} rejected. Added to simulated_missions.csv as inactive.")
            self.update_stats()
        else:
            messagebox.showwarning("Warning", "No primary mission to reject.")
    
    def update_conflict_tree(self, conflicted_missions):
        self.conflict_tree.delete(*self.conflict_tree.get_children())
        
        for mission in conflicted_missions:
            self.conflict_tree.insert("", "end", values=(
                mission.mission_id,
                mission.start_time.strftime("%Y-%m-%d %H:%M"),
                f"{mission.duration.total_seconds()/60:.0f} min",
                mission.status,
                mission.status_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "Click Abort to resolve"
            ))
    
    def update_status(self, message):
        self.status_text.delete(1.0, tk.END)
        self.status_text.insert(1.0, f"{datetime.now().strftime('%H:%M:%S')} - {message}")
    
    def update_stats(self):
        stats = self.dcs.get_mission_statistics()
        
        stats_text = f"""
Total Missions in simulated_missions.csv: {stats['total_simulated']}
Status: Active: {stats['active_missions']} | Aborted: {stats['aborted_missions']} | Inactive: {stats['inactive_missions']} | Completed: {stats['completed_missions']}
Active Missions in airspace_data.csv: {stats['airspace_missions']}
Primary Mission: {stats['primary_mission'] or 'None'}
Current Conflicts: {stats['current_conflicts']}

CSV Files Usage:
- simulated_missions.csv: All missions with status (active/aborted/inactive) - Total: {stats['total_simulated']}
- airspace_data.csv: Only active missions (accepted missions) - Total: {stats['airspace_missions']}
        """
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(1.0, stats_text.strip())

def main():
    root = tk.Tk()
    app = DCSGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()