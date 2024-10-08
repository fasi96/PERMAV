import streamlit as st
import pandas as pd
import plotly.express as px

# Life Units
life_units = [
    "Significant Other", "Family", "Friendship", 
    "Physical Health/Sports", "Mental Health/Mindfulness", "Spirituality/Faith", 
    "Community/Citizenship", "Societal Engagement", "Job/Career", 
    "Education/Learning", "Finances", "Hobbies/Interests", 
    "Online Entertainment", "Offline Entertainment", "Physiological Needs", 
    "Activities of Daily Living"
]

st.title("Strategic Life Units - Importance, Satisfaction, and Time Spent")

# Initialize session state
if 'current_unit_index' not in st.session_state:
    st.session_state.current_unit_index = 0
    st.session_state.data = pd.DataFrame(columns=['Life Unit', 'Importance', 'Satisfaction', 'Time Spent'])

# Function to add data for a life unit
def add_life_unit_data(unit, importance, satisfaction, time_spent):
    new_data = pd.DataFrame({
        'Life Unit': [unit],
        'Importance': [int(importance)],
        'Satisfaction': [int(satisfaction)],
        'Time Spent': [float(time_spent)]  # Ensure Time Spent is a float
    })
    if unit in st.session_state.data['Life Unit'].values:
        # Update the existing row
        st.session_state.data.loc[st.session_state.data['Life Unit'] == unit, ['Importance', 'Satisfaction', 'Time Spent']] = [int(importance), int(satisfaction), float(time_spent)]
    else:
        # Append a new row
        st.session_state.data = pd.concat([st.session_state.data, new_data], ignore_index=True)

# Display input form for current life unit
if st.session_state.current_unit_index < len(life_units):
    current_unit = life_units[st.session_state.current_unit_index]
    st.header(f"Rate {current_unit}")
    
    # Get existing values if available
    existing_data = st.session_state.data[st.session_state.data['Life Unit'] == current_unit]
    importance = st.slider(f"Importance of {current_unit}", 0, 10, 
                           int(existing_data['Importance'].values[0]) if not existing_data.empty else 5)
    satisfaction = st.slider(f"Satisfaction with {current_unit}", 0, 10, 
                             int(existing_data['Satisfaction'].values[0]) if not existing_data.empty else 5)
    time_spent = st.number_input(f"Time spent on {current_unit} (hours/week)", 0.0, 168.0, 
                                 float(existing_data['Time Spent'].values[0]) if not existing_data.empty else 10.0)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Previous") and st.session_state.current_unit_index > 0:
            add_life_unit_data(current_unit, importance, satisfaction, time_spent)
            st.session_state.current_unit_index -= 1
            st.rerun()
    with col2:
        if st.button("Next"):
            add_life_unit_data(current_unit, importance, satisfaction, time_spent)
            st.session_state.current_unit_index += 1
            st.rerun()

# Display summary and visualization when all units are rated
else:
    st.header("Summary")
    st.dataframe(st.session_state.data)
    
    st.header("Visualization")
    
    # Ensure 'Time Spent' is numeric
    st.session_state.data['Time Spent'] = pd.to_numeric(st.session_state.data['Time Spent'], errors='coerce')
    
    fig = px.scatter(
        st.session_state.data,
        x='Satisfaction',
        y='Importance',
        size='Time Spent',
        color='Life Unit',
        hover_name='Life Unit',
        hover_data=['Importance', 'Satisfaction', 'Time Spent'],
        size_max=60,
        title='Strategic Life Units'
    )
    
    # Add quadrant lines
    fig.add_hline(y=5, line_dash="dot", line_color="gray", opacity=0.5)
    fig.add_vline(x=5, line_dash="dot", line_color="gray", opacity=0.5)
    
    # Add quadrant labels
    fig.add_annotation(x=2.5, y=7.5, text="High Importance,<br>Low Satisfaction", showarrow=False, font=dict(size=10))
    fig.add_annotation(x=7.5, y=7.5, text="High Importance,<br>High Satisfaction", showarrow=False, font=dict(size=10))
    fig.add_annotation(x=2.5, y=2.5, text="Low Importance,<br>Low Satisfaction", showarrow=False, font=dict(size=10))
    fig.add_annotation(x=7.5, y=2.5, text="Low Importance,<br>High Satisfaction", showarrow=False, font=dict(size=10))
    
    fig.update_layout(
        xaxis_title='Satisfaction',
        yaxis_title='Importance',
        xaxis=dict(range=[0, 10]),
        yaxis=dict(range=[0, 10])
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    if st.button("Start Over"):
        st.session_state.current_unit_index = 0
        st.session_state.data = pd.DataFrame(columns=['Life Unit', 'Importance', 'Satisfaction', 'Time Spent'])
        st.rerun()

# Progress bar
progress = st.session_state.current_unit_index / len(life_units)
st.progress(progress)
