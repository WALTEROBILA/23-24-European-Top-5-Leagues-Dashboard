import pandas as pd
import streamlit as st 
import matplotlib.pyplot as plt
import functions
import plotly.graph_objects as go
import altair as alt
from soccerplots.radar_chart import Radar

# Data Importation
## Ligue 1
### Raw
li_defe = pd.read_excel("data/li_defensive_actions.xlsx", sheet_name="raw")
li_std=pd.read_excel("data/li_standard.xlsx", sheet_name="raw")
li_poss = pd.read_excel("data/li_possession.xlsx", sheet_name="raw")
li_pass = pd.read_excel("data/li_passing.xlsx", sheet_name="raw")
li_ptype=pd.read_excel("data/li_pass_types.xlsx", sheet_name="raw")
li_misc = pd.read_excel("data/li_misc.xlsx", sheet_name="raw")
li_league = "Ligue 1"
### Per 90
li_defe_1 = pd.read_excel("data/li_defensive_actions.xlsx", sheet_name="per_90")
li_std_1 =pd.read_excel("data/li_standard.xlsx", sheet_name="per_90")
li_poss_1 = pd.read_excel("data/li_possession.xlsx", sheet_name="per_90")
li_pass_1 = pd.read_excel("data/li_passing.xlsx", sheet_name="per_90")
li_ptype_1 =pd.read_excel("data/li_pass_types.xlsx", sheet_name="per_90")
li_misc_1 = pd.read_excel("data/li_misc.xlsx", sheet_name="per_90")
li_league_1 = "Ligue 1"


## Premier League
### Raw
pl_defe = pd.read_excel("data/pl_defensive_actions.xlsx", sheet_name="raw")
pl_std=pd.read_excel("data/pl_standard.xlsx", sheet_name="raw")
pl_poss = pd.read_excel("data/pl_possession.xlsx", sheet_name="raw")
pl_pass = pd.read_excel("data/pl_passing.xlsx", sheet_name="raw")
pl_ptype=pd.read_excel("data/pl_pass_types.xlsx", sheet_name="raw")
pl_misc = pd.read_excel("data/pl_misc.xlsx", sheet_name="raw")
pl_league = "Premier League"
### Raw
pl_defe_1 = pd.read_excel("data/pl_defensive_actions.xlsx", sheet_name="per_90")
pl_std_1 =pd.read_excel("data/pl_standard.xlsx", sheet_name="per_90")
pl_poss_1 = pd.read_excel("data/pl_possession.xlsx", sheet_name="per_90")
pl_pass_1 = pd.read_excel("data/pl_passing.xlsx", sheet_name="per_90")
pl_ptype_1 =pd.read_excel("data/pl_pass_types.xlsx", sheet_name="per_90")
pl_misc_1 = pd.read_excel("data/pl_misc.xlsx", sheet_name="per_90")
pl_league_1 = "Premier League"

li = functions.merge_stats(league=li_league,
                           std=li_std,
                           poss=li_poss,
                           pas=li_pass,
                           ptype=li_ptype,
                           misc=li_misc,
                           defe=li_defe)
li_1 = functions.merge_stats(league=li_league_1,
                           std=li_std_1,
                           poss=li_poss_1,
                           pas=li_pass_1,
                           ptype=li_ptype_1,
                           misc=li_misc_1,
                           defe=li_defe_1)

pl = functions.merge_stats(league=pl_league,
                           std=pl_std,
                           poss=pl_poss,
                           pas=pl_pass,
                           ptype=pl_ptype,
                           misc=pl_misc,
                           defe=pl_defe)
pl_1 = functions.merge_stats(league=pl_league_1,
                           std=pl_std_1,
                           poss=pl_poss_1,
                           pas=pl_pass_1,
                           ptype=pl_ptype_1,
                           misc=pl_misc_1,
                           defe=pl_defe_1)

data = functions.merge_leagues(pl=pl, li=li)
dat = functions.merge_leagues(pl=pl_1, li=li_1)

#print(data["League"].unique())

league, z,team = st.columns(3)
with league:
    league = st.selectbox("Select League:", data["League"].unique())

filtered = data[data["League"]==league]

with team:
    team = st.selectbox("Select Club:", filtered["Squad"].unique())


gls, g_a, ast = st.columns(3)

#Goals Table
with gls:
    
    gl = filtered[["Player", "Goals Scored","League","Squad"]]
    gls = gl[(gl["League"]==league) & (gl["Squad"]==team)].sort_values(by="Goals Scored", ascending=False)
    fig = go.Figure(data=[go.Table(
    header=dict(
        values=["Player","Goals Scored"],
        fill_color='Black',
        align='left'
    ),
    cells=dict(
        values=[gls['Player'], gls['Goals Scored']],
        fill_color='Black',
        align='left'
    )
    )])
    fig.update_layout(title="Scoring Charts", width=400)
    st.plotly_chart(fig)

#Assists Table
with ast:
    
    asts = filtered[["Player", "Assists", "League","Squad"]]
    ast = asts[(asts["League"]==league) & (asts["Squad"]==team)].sort_values(by = "Assists", ascending=False)
    fg = go.Figure(data=[go.Table(
    header=dict(
        values=["Player","Assists"],
        fill_color='Black',
        align='left'
    ),
    cells=dict(
        values=[ast['Player'], ast['Assists']],
        fill_color='Black',
        align='left'
    )
    )])
    fg.update_layout(title="Assists Charts", width = 400)
    st.plotly_chart(fg)
    

minu=st.slider("Select Minimum Minutes Played:",min_value=100, max_value= max(dat["Minutes Played"]),step=100, value=900)
st.markdown(f"### These stats are presented per 90 minutes for players accumulating a minimum of **{minu}** minutes across the league campaign")
dat = dat[dat["Minutes Played"]>minu]
one, two, three = st.columns(3)

# Goals and Assist per 90.


with one:
    st.subheader("Goals and Assists per 90")
    ga = dat[["Player","Squad","Goals Scored","Assists","League"]]

    color_scale = alt.Scale(
        domain = ["Premier League","Ligue 1","La Liga", "Serie A", "Bundesliga"],
        range = ["#FF0000","#00FFFF","#008000","#FFA500","#FFFF00"]
    )
    chart = alt.Chart(ga).mark_point().encode(
        x = "Goals Scored", y = 'Assists', color = alt.Color("League", scale=color_scale),
        tooltip=["Player","Goals Scored","Assists"]).properties(title="Goals and Assists per 90")

    #text = chart.mark_text(
    #    align = "left",
    #    baseline = "middle",
    #    dx = 7
    #).encode(text="Player")
        
    st.altair_chart(chart)


# Comparing two metrics

dat1 = functions.scatter_variables(dat)
with three:
    ex,yai = st.columns(2)

    

    with ex:
        default_index = 12 if len(dat1.iloc[:,1:]) > 12 else 0
        x = st.selectbox("Select a metric", dat1.iloc[:,1:].columns,index=default_index)
    with yai:
        default_index_1 = 13 if len(dat1.iloc[:,1:]) > 13 else 0
        y = st.selectbox("Select metric", dat1.iloc[:,1:].columns,index=default_index_1)

    color_scale = alt.Scale(
        domain = ["Premier League","Ligue 1","La Liga", "Serie A", "Bundesliga"],
        range = ["#FF0000","#00FFFF","#008000","#FFA500","#FFFF00"]
    )
    scatter = alt.Chart(dat1).mark_point().encode(
        x = x, y = y, color = alt.Color("League", scale=color_scale),
        tooltip=["Player",x,y]).properties(title=f"{x} per 90 vs {y} per 90, Minimum {minu} minutes", width =700)
    st.altair_chart(scatter)    


### Radar Chart

template = st.radio("Select a template:",["Attacking Template","Possession Template","Defensive Template"])

p1, p3,p2 = st.columns(3)
with p1:
    player_1 = st.selectbox("Select player:",dat["Player"].unique(), index = 55)
with p2:
    player_2 = st.selectbox("Select Player:",dat["Player"].unique(), index = 70)


if template == "Attacking Template":
    rdat = dat1[["Player","Squad","Goals Scored","Assists","Dribbles Attempted","Dribble Success %","Key Passes","Crosses into the Penalty Area",
            "Passes into the Penalty Area","Expected Goals","Expected Assists","Assists Overperformance"]]
elif template == "Possession Template":
    rdat = dat1[["Player","Squad","Pass Completion %","Progressive Passes","Carries","Progressive Carries","Progressive Carrying Distance",
                "Progressive Passing Distance","Through Balls","Touches","Progressive Passes Received","Key Passes",]]
elif template == "Defensive Template":
    rdat = dat1[["Player","Squad","Recoveries","Tackles","Tackles Won","Tackle Success Rate","Interceptions","Clearances","Errors Leading to a Shot",
                "Fouls","Aerial Duel Success Rate"]]


functions.comparison_radar(rdat=rdat, player_1=player_1, player_2=player_2)




































