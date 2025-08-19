import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime
from urllib.parse import urlparse

# Check if required packages are installed
try:
    import snowflake.connector
    SNOWFLAKE_AVAILABLE = True
except ImportError:
    SNOWFLAKE_AVAILABLE = False

# Demo data for when Snowflake is not available
def get_demo_data():
    teams = [
        (1, "Red Bull Racing", 150000.00),
        (2, "Mercedes-AMG", 145000.00),
        (3, "Ferrari", 140000.00),
        (4, "McLaren", 120000.00),
        (5, "Alpine", 100000.00)
    ]
    
    cars = [
        (1, "Red Bull Racing", "RB19", 350, 1050, 85, 90),
        (2, "Red Bull Racing", "RB18", 345, 1020, 80, 95),
        (3, "Mercedes-AMG", "W14", 348, 1040, 85, 88),
        (4, "Mercedes-AMG", "W13", 346, 1030, 80, 87),
        (5, "Ferrari", "SF-23", 352, 1060, 80, 87)
    ]
    
    races = [
        (1, "Monaco Grand Prix", 100, "Asphalt", 1000.00, 5000.00),
        (2, "Swedish Rally", 120, "Snow", 1500.00, 6000.00),
        (3, "Safari Rally Kenya", 110, "Gravel", 1200.00, 5500.00)
    ]
    
    return teams, cars, races

@st.cache_resource
def init_connection():
    try:
        # Check if secrets are configured
        if 'snowflake' not in st.secrets:
            st.error("Snowflake credentials not found in secrets!")
            return None
        
        # Get account from secrets and clean it
        raw_account = st.secrets["snowflake"]["account"]
        
        # Parse the account from URL if it's a full URL
        if raw_account.startswith('https://'):
            parsed_url = urlparse(raw_account)
            account = parsed_url.netloc.replace('.snowflakecomputing.com', '')
        else:
            account = raw_account
        
        st.sidebar.info(f"Connecting to account: {account}")
            
        # Connect to Snowflake
        conn = snowflake.connector.connect(
            user=st.secrets["snowflake"]["user"],
            password=st.secrets["snowflake"]["password"],
            account=st.secrets["snowflake"]["account"],
            role=st.secrets["snowflake"]["role"],
            warehouse=st.secrets["snowflake"]["warehouse"],
            database=st.secrets["snowflake"]["database"],
            schema=st.secrets["snowflake"].get("schema", "PUBLIC"),
            client_session_keep_alive=True
        )
        
        # Test the connection with a simple query
        with conn.cursor() as cur:
            cur.execute("SELECT CURRENT_VERSION()")
            version = cur.fetchone()
            st.sidebar.success(f"✅ Connected to Snowflake v{version[0]}")
            
        return conn
        
    except snowflake.connector.errors.DatabaseError as db_err:
        st.error(f"Database error: {db_err}")
        return None
    except snowflake.connector.errors.ProgrammingError as prog_err:
        st.error(f"Programming error: {prog_err}")
        return None
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        return None

# Perform query with better error handling
@st.cache_data(ttl=600)
def run_query(query, _conn):
    try:
        with _conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()
    except Exception as e:
        st.error(f"Query failed: {str(e)}")
        return []

# Execute query without returning results
def execute_query(query, _conn):
    try:
        with _conn.cursor() as cur:
            cur.execute(query)
        return True
    except Exception as e:
        st.error(f"Query execution failed: {str(e)}")
        return False

# Get teams for dropdown
def get_teams(_conn):
    query = "SELECT team_id, team_name FROM bootcamp_rally.teams.teams ORDER BY team_name"
    return run_query(query, _conn)

# Get cars with team names
def get_cars(_conn):
    query = """
    SELECT c.car_id, t.team_name, c.model, c.speed, c.horsepower, c.handling, c.durability
    FROM bootcamp_rally.cars.cars c
    JOIN bootcamp_rally.teams.teams t ON c.team_id = t.team_id
    ORDER BY t.team_name, c.model
    """
    return run_query(query, _conn)

# Add new car
def add_car(_conn, team_id, model, speed, horsepower, handling, durability):
    query = f"""
    INSERT INTO bootcamp_rally.cars.cars (team_id, model, speed, horsepower, handling, durability)
    VALUES ({team_id}, '{model}', {speed}, {horsepower}, {handling}, {durability})
    """
    return execute_query(query, _conn)

# Add new team
def add_team(_conn, team_name, budget):
    query = f"""
    INSERT INTO bootcamp_rally.teams.teams (team_name, budget)
    VALUES ('{team_name}', {budget})
    """
    return execute_query(query, _conn)

# Get team budgets
def get_team_budgets(_conn):
    query = "SELECT team_id, team_name, budget FROM bootcamp_rally.teams.teams ORDER BY team_name"
    return run_query(query, _conn)

# Update team budget
def update_team_budget(_conn, team_id, new_budget):
    query = f"""
    UPDATE bootcamp_rally.teams.teams
    SET budget = {new_budget}
    WHERE team_id = {team_id}
    """
    return execute_query(query, _conn)

# Get available races
def get_races(_conn):
    query = "SELECT race_id, race_name, track_length_km, track_type, participation_fee, prize_pool FROM bootcamp_rally.races.races ORDER BY race_name"
    return run_query(query, _conn)

# Simulate race
def simulate_race(_conn, race_id):
    # Get race details
    race_query = f"""
    SELECT race_name, track_length_km, track_type, participation_fee, prize_pool 
    FROM bootcamp_rally.races.races 
    WHERE race_id = {race_id}
    """
    race_details = run_query(race_query, _conn)
    if not race_details:
        return "Race not found!"
    
    race_name, track_length, track_type, fee, prize_pool = race_details[0]
    
    # Get all cars with their teams
    cars_query = """
    SELECT c.car_id, t.team_id, t.team_name, c.model, c.speed, c.horsepower, c.handling, c.durability, t.budget
    FROM bootcamp_rally.cars.cars c
    JOIN bootcamp_rally.teams.teams t ON c.team_id = t.team_id
    """
    all_cars = run_query(cars_query, _conn)
    
    # Check if teams can afford participation fee
    participants = []
    for car in all_cars:
        car_id, team_id, team_name, model, speed, hp, handling, durability, budget = car
        if budget >= fee:
            participants.append({
                'car_id': car_id,
                'team_id': team_id,
                'team_name': team_name,
                'model': model,
                'speed': speed,
                'horsepower': hp,
                'handling': handling,
                'durability': durability,
                'budget': budget
            })
            # Deduct participation fee
            new_budget = budget - fee
            update_team_budget(_conn, team_id, new_budget)
    
    if not participants:
        return "No teams can afford to participate in the race!"
    
    # Simulate race for each participant
    results = []
    for car in participants:
        # Base performance based on car characteristics
        base_performance = (
            car['speed'] * 0.3 +
            car['horsepower'] * 0.2 +
            car['handling'] * 0.3 +
            car['durability'] * 0.2
        )
        
        # Adjust for track type
        track_factor = 1.0
        if track_type == 'Snow':
            track_factor = car['handling'] / 100
        elif track_type == 'Gravel':
            track_factor = car['durability'] / 100
        
        # Random factor (0.8 to 1.2)
        random_factor = random.uniform(0.8, 1.2)
        
        # Calculate finish time (lower is better)
        finish_time = (track_length * 1000) / (base_performance * track_factor * random_factor)
        
        results.append({
            'car_id': car['car_id'],
            'team_id': car['team_id'],
            'team_name': car['team_name'],
            'model': car['model'],
            'finish_time': finish_time,
            'budget': car['budget'] - fee  # Updated after fee deduction
        })
    
    # Sort by finish time (ascending)
    results.sort(key=lambda x: x['finish_time'])
    
    # Assign positions and prizes
    prize_distribution = [0.4, 0.3, 0.2, 0.1]  # Top 4 get prizes
    for i, result in enumerate(results):
        result['position'] = i + 1
        if i < len(prize_distribution):
            prize = prize_pool * prize_distribution[i]
            result['prize'] = prize
            # Update team budget with prize money
            new_budget = result['budget'] + prize
            update_team_budget(_conn, result['team_id'], new_budget)
        else:
            result['prize'] = 0
    
    # Record race results
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    execute_query(f"INSERT INTO bootcamp_rally.races.races (race_name, track_length_km, track_type, participation_fee, prize_pool, race_date) VALUES ('{race_name}', {track_length}, '{track_type}', {fee}, {prize_pool}, '{current_time}')", _conn)
    
    # Get the last inserted race_id
    race_id_query = "SELECT MAX(race_id) FROM bootcamp_rally.races.races"
    new_race_id = run_query(race_id_query, _conn)[0][0]
    
    # Insert results
    for result in results:
        execute_query(f"""
        INSERT INTO bootcamp_rally.races.race_results (race_id, car_id, team_id, finish_time, position, prize_awarded)
        VALUES ({new_race_id}, {result['car_id']}, {result['team_id']}, {result['finish_time']}, {result['position']}, {result['prize']})
        """, _conn)
    
    return results

# Streamlit app
def main():
    st.set_page_config(page_title="Rally Racing Management", page_icon="🏎️", layout="wide")
    st.title("🏎️ Bootcamp Rally Racing Management")
    
    # Check if Snowflake connector is available
    if not SNOWFLAKE_AVAILABLE:
        st.warning("Snowflake connector not available. Running in demo mode.")
        demo_mode = True
        conn = None
        teams, cars, races = get_demo_data()
    else:
        # Initialize connection
        conn = init_connection()
        demo_mode = conn is None
        
        if demo_mode:
            teams, cars, races = get_demo_data()
        else:
            # Test if we can access the database
            try:
                test_query = "SHOW DATABASES LIKE 'BOOTCAMP_RALLY'"
                result = run_query(test_query, conn)
                if not result:
                    st.error("BOOTCAMP_RALLY database not found! Please run the SQL scripts first.")
                    demo_mode = True
                    teams, cars, races = get_demo_data()
            except:
                st.error("Cannot access BOOTCAMP_RALLY database. Running in demo mode.")
                demo_mode = True
                teams, cars, races = get_demo_data()
    
    # Sidebar navigation
    page = st.sidebar.selectbox("Navigation", ["Dashboard", "Manage Teams", "Manage Cars", "Run Race", "View Results"])

    if page == "Dashboard":
        st.header("🏁 Rally Racing Dashboard")
        
        # Display teams and budgets
        st.subheader("🏆 Teams & Budgets")
        if demo_mode:
            team_df = pd.DataFrame(teams, columns=["ID", "Team Name", "Budget ($)"])
        else:
            teams_data = get_team_budgets(conn) if conn else []
            if teams_data:
                team_df = pd.DataFrame(teams_data, columns=["ID", "Team Name", "Budget ($)"])
            else:
                st.info("No teams found in the database.")
                team_df = pd.DataFrame()
        
        if not team_df.empty:
            st.dataframe(team_df, hide_index=True)
        
        # Display cars
        st.subheader("🚗 Cars")
        if demo_mode:
            car_df = pd.DataFrame(cars, columns=["ID", "Team", "Model", "Speed", "Horsepower", "Handling", "Durability"])
        else:
            cars_data = get_cars(conn) if conn else []
            if cars_data:
                car_df = pd.DataFrame(cars_data, columns=["ID", "Team", "Model", "Speed", "Horsepower", "Handling", "Durability"])
            else:
                st.info("No cars found in the database.")
                car_df = pd.DataFrame()
        
        if not car_df.empty:
            st.dataframe(car_df, hide_index=True)
        
        # Display upcoming races
        st.subheader("📅 Upcoming Races")
        if demo_mode:
            race_df = pd.DataFrame(races, columns=["ID", "Race Name", "Length (km)", "Track Type", "Fee ($)", "Prize Pool ($)"])
        else:
            races_data = get_races(conn) if conn else []
            if races_data:
                race_df = pd.DataFrame(races_data, columns=["ID", "Race Name", "Length (km)", "Track Type", "Fee ($)", "Prize Pool ($)"])
            else:
                st.info("No races found in the database.")
                race_df = pd.DataFrame()
        
        if not race_df.empty:
            st.dataframe(race_df, hide_index=True)

    elif page == "Manage Teams":
        st.header("👥 Manage Teams")
        
        if demo_mode:
            st.warning("This feature is not available in demo mode. Connect to Snowflake to manage teams.")
        else:
            # Add new team form
            with st.form("add_team_form"):
                st.subheader("➕ Add New Team")
                team_name = st.text_input("Team Name")
                budget = st.number_input("Initial Budget ($)", min_value=0, value=10000)
                submitted = st.form_submit_button("Add Team")
                
                if submitted:
                    if team_name:
                        if add_team(conn, team_name, budget):
                            st.success(f"Team '{team_name}' added with budget ${budget}!")
                            st.rerun()
                        else:
                            st.error("Failed to add team. Please check your database connection.")
                    else:
                        st.error("Please enter a team name.")
            
            # Display current teams
            st.subheader("📋 Current Teams")
            teams_data = get_team_budgets(conn) if conn else []
            if teams_data:
                team_df = pd.DataFrame(teams_data, columns=["ID", "Team Name", "Budget ($)"])
                st.dataframe(team_df, hide_index=True)
            else:
                st.info("No teams found in the database.")

    elif page == "Manage Cars":
        st.header("🚗 Manage Cars")
        
        if demo_mode:
            st.warning("This feature is not available in demo mode. Connect to Snowflake to manage cars.")
        else:
            # Add new car form
            with st.form("add_car_form"):
                st.subheader("➕ Add New Car")
                
                # Get teams for dropdown
                teams_data = get_teams(conn) if conn else []
                if not teams_data:
                    st.error("No teams available. Please add teams first.")
                else:
                    team_options = {f"{team_id} - {name}": team_id for team_id, name in teams_data}
                    selected_team = st.selectbox("Team", options=list(team_options.keys()))
                    
                    model = st.text_input("Car Model")
                    col1, col2 = st.columns(2)
                    with col1:
                        speed = st.slider("Speed", 1, 500, 300)
                        horsepower = st.slider("Horsepower", 1, 2000, 800)
                    with col2:
                        handling = st.slider("Handling", 1, 100, 75)
                        durability = st.slider("Durability", 1, 100, 80)
                    
                    submitted = st.form_submit_button("Add Car")
                    
                    if submitted:
                        if model:
                            team_id = team_options[selected_team]
                            if add_car(conn, team_id, model, speed, horsepower, handling, durability):
                                st.success(f"Car '{model}' added to team!")
                                st.rerun()
                            else:
                                st.error("Failed to add car. Please check your database connection.")
                        else:
                            st.error("Please enter a car model.")
            
            # Display current cars
            st.subheader("📋 Current Cars")
            cars_data = get_cars(conn) if conn else []
            if cars_data:
                car_df = pd.DataFrame(cars_data, columns=["ID", "Team", "Model", "Speed", "Horsepower", "Handling", "Durability"])
                st.dataframe(car_df, hide_index=True)
            else:
                st.info("No cars found in the database.")

    elif page == "Run Race":
        st.header("🏁 Run Race")
        
        if demo_mode:
            st.warning("This feature is not available in demo mode. Connect to Snowflake to run races.")
        else:
            # Select race
            races_data = get_races(conn) if conn else []
            if not races_data:
                st.warning("No races available. Please add races to the database.")
            else:
                race_options = {f"{race_id} - {name}": race_id for race_id, name, length, track_type, fee, prize in races_data}
                selected_race = st.selectbox("Select Race", options=list(race_options.keys()))
                
                if st.button("Start Race! 🏎️💨"):
                    race_id = race_options[selected_race]
                    
                    # Show loading animation
                    with st.spinner("Race in progress..."):
                        # Simulate race with progress bar
                        progress_bar = st.progress(0)
                        for percent_complete in range(100):
                            time.sleep(0.02)  # Simulate race progress
                            progress_bar.progress(percent_complete + 1)
                        
                        # Get race results
                        results = simulate_race(conn, race_id)
                    
                    if isinstance(results, str):
                        st.error(results)
                    else:
                        st.success("Race completed! 🏁")
                        
                        # Display results
                        st.subheader("📊 Race Results")
                        results_df = pd.DataFrame(results)
                        results_df = results_df[['position', 'team_name', 'model', 'finish_time', 'prize']]
                        results_df['finish_time'] = results_df['finish_time'].round(2)
                        results_df['prize'] = results_df['prize'].round(2)
                        results_df.columns = ['Position', 'Team', 'Car Model', 'Finish Time (s)', 'Prize ($)']
                        
                        st.dataframe(results_df, hide_index=True)
                        
                        # Show podium
                        st.subheader("🏆 Podium")
                        cols = st.columns(3)
                        if len(results) > 0:
                            with cols[0]:
                                st.subheader("2nd 🥈")
                                st.write(f"{results[1]['team_name']}")
                                st.write(f"{results[1]['model']}")
                        if len(results) > 0:
                            with cols[1]:
                                st.subheader("1st 🥇")
                                st.write(f"{results[0]['team_name']}")
                                st.write(f"{results[0]['model']}")
                        if len(results) > 2:
                            with cols[2]:
                                st.subheader("3rd 🥉")
                                st.write(f"{results[2]['team_name']}")
                                st.write(f"{results[2]['model']}")

    elif page == "View Results":
        st.header("📋 Race Results History")
        
        if demo_mode:
            st.warning("This feature is not available in demo mode. Connect to Snowflake to view results.")
        else:
            # Get all past race results
            query = """
            SELECT r.race_name, rr.position, t.team_name, c.model, rr.finish_time, rr.prize_awarded
            FROM bootcamp_rally.races.race_results rr
            JOIN bootcamp_rally.races.races r ON rr.race_id = r.race_id
            JOIN bootcamp_rally.teams.teams t ON rr.team_id = t.team_id
            JOIN bootcamp_rally.cars.cars c ON rr.car_id = c.car_id
            ORDER BY r.race_date DESC, rr.position
            """
            
            results = run_query(query, conn) if conn else []
            
            if results:
                results_df = pd.DataFrame(results, columns=["Race", "Position", "Team", "Car Model", "Finish Time", "Prize ($)"])
                results_df['Finish Time'] = results_df['Finish Time'].round(2)
                st.dataframe(results_df, hide_index=True)
            else:
                st.info("No race results available yet. Run a race first!")

if __name__ == "__main__":
    main()