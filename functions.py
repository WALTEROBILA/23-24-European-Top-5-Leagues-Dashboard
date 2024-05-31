import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import soccerplots
from soccerplots.radar_chart import Radar



def clean_standard(std):
    """
    Cleans "Standard Stats" data, renaming columns.\n

    Args:
        Standard Stats data. \n
    
    Returns:
        Renamed Standard Stats data.
    """
    std.rename(columns={"Gls":"Goals Scored", "Ast":"Assists","G+A":"Goals + Assists","Min":"Minutes Played", "xG":"Expected Goals","xAG":"Expected Assists","PK":"Penalties Scored","PKatt":"Penalties Attempted","CrdY":"Yellow Cards", "CrdR":"Red Cards",
                         "PrgC":"Progressive Carries","PrgP":"Progressive Passes","PrgR":"Progressive Passes Received", "G-PK":"Non-Penalty Goals",
                          "npxG":"Non-Penalty Expected Goals", }, inplace=True)
    return std

def clean_poss(poss):
    """
    Cleans "Possession" data, renaming columns and dropping a few from the data.\n

    Args:
        Possession data. \n
    
    Returns:
        Cleaned Possesion data.
    """
    poss.rename(columns={"Att 3rd":"Touches in the Attacking Third", "TotDist":"Total Carry Distance","Att":"Dribbles Attempted", "Succ%":"Dribble Success %",
                         "1/3":"Carries Into the Final Third", "CPA":"Carries into the Penalty Area","Rec":"Passes Received",
                         "PrgR":"Progressive Passes Received","Def Pen":"Touches in the Defensive Penalty Area",
                         "Def 3rd":"Defensive 1/3 Touches","Mid 3rd":"Middle 1/3 Touches","Att Pen":"Attacking Penalty Area Touches",},inplace=True)
    poss.drop(columns=["Pos","Age","Born","90s","Nation","Matches"], inplace=True)
    return poss

def clean_pass(pas):
    """
    Cleans "Passing" data, renaming columns and dropping a few.\n

    Args:
        Passing data. \n
    
    Returns:
        Cleaned Passing data.
    """
    pas.rename(columns={"KP":"Key Passes","CrsPA":"Crosses into the Penalty Area","PPA":"Passes into the Penalty Area",
                        "A-xAG":"Assists Overperformance","Att":"Passes Attempted",
                        "Cmp%":"Pass Completion %"},inplace=True)
    pas.drop(columns=["Pos","Age","Born","90s","Nation","Matches"], inplace=True)
    return pas

def clean_ptypes(ptype):
    """
    Cleans "Pass Types" data, renaming columns and dropping a few.\n

    Args:
        Pass Types data. \n
    
    Returns:
        Cleaned Pass Types data.
    """
    ptype.rename(columns={"Sw":"Switches"},inplace=True)
    ptype.drop(columns=["Pos","Age","Born","90s","Nation","Att","Matches"], inplace=True)
    return ptype

def clean_misc(misc):
    """
    Cleans miscellanaous data, renaming columns and dropping a few.\n

    Args:
        Miscellanous data. \n
    
    Returns:
        Cleaned Miscellanous data.
    """
    misc.rename(columns={"Recov":"Recoveries","Won%":"Aerial Duel Success Rate","Fls":"Fouls", "'Int":"Interceptions", "Fld":"Fouls Drawn","PKwon":"Penalty Kicks Won"}, inplace=True)
    misc.drop(columns=["Pos","Age","Born","90s","Nation","Matches"], inplace=True)
    return misc
    
def clean_def_actions(defe):
    """
    Cleans "defensive actions" data, renaming columns, dropping a few and generating a new feature.\n

    Args:
        Defensive Actions data. \n
    
    Returns:
        Cleaned Defensive Actions data.
    """
    defe.rename(columns={"Tkl":"Tackles"},inplace=True)
    defe.drop(columns=["Pos","Age","Born","90s","Nation","Matches"], inplace=True)
    defe['Tackle Success Rate'] = (defe['TklW']/defe["Tackles"]) * 100
    return defe


def merge_stats(league, std, poss, pas, ptype, misc, defe):
    """
    Combines the standard stats, possession, passing, pass types, miscellanous and defensive actions data, merging them into 
    a single dataframe. Also adds a "League" variable to the data, specifying the league in which the player plays, as at
    the time of collection of the data.\n

    Args:
        league=league
        std, poss, pas, ptype, misc, and defe dataframes. All should have been passed through the functions.\n

    Returns:
        A dataframe with all all attributes stated above, as well as the league. 
    """
    std = clean_standard(std)
    poss = clean_poss(poss)
    pas = clean_pass(pas)
    ptype = clean_ptypes(ptype)
    misc = clean_misc(misc)
    defe = clean_def_actions(defe)

    data = std.merge(poss, on=["Player","Squad"], how="left")
    data = data.merge(pas, on=["Player", "Squad"], how="left")
    data = data.merge(ptype, on=["Player","Squad"], how="left")
    data = data.merge(misc, on=["Player","Squad"], how="left")
    data = data.merge(defe, on=["Player", "Squad"], how="left")
    data["League"] = league
    return data


def merge_leagues(pl,li):
    """
    Merges dataframes from different leagues.\n

    Args:
        pl,li,ll,sa,bl = Premier League, Liggue 1, La Liga, Serie A, Bundesliga dataframes.\n

    Returns:
        A unified dataframe with all leagues.
    """
    data = pd.concat([pl,li], axis=0)
    print(data["League"].unique())
    return data

def scatter_variables(data):    # Variables to appear on the x,y scatterplot
    """
    A function  that defines the data that will appear on the scatterplots, as well as the radar plots. The data should ideally be per 90. \n

    Args:
        A cleaned dataset that contains data from various leagues.\n

    Returns:
        Data to be plotted on the scatterplots as well as comparative radar plots.
    """
    dat = data[["Player","Squad","Goals Scored","Assists","Goals + Assists", "Non-Penalty Goals","Penalties Scored","Penalties Attempted",
               "Yellow Cards", "Red Cards","Expected Goals","Non-Penalty Expected Goals","Expected Assists",
               "Progressive Carries","Progressive Passes","Progressive Passes Received_x","Touches","Touches in the Defensive Penalty Area",
               "Defensive 1/3 Touches","Middle 1/3 Touches","Touches in the Attacking Third","Attacking Penalty Area Touches",
               "Dribbles Attempted","Dribble Success %","Carries", "Total Carry Distance","PrgDist_x","PrgC","Carries into the Penalty Area",
                "Passes Received","Passes Attempted","Pass Completion %","TotDist",
                "PrgDist_y","Cmp.1","Att.1","Cmp%.1","Cmp.2","Att.2","Cmp%.2","Cmp.3","Att.3","Cmp%.3","Assists Overperformance",
                "Key Passes","Passes into the Penalty Area","Crosses into the Penalty Area","Live_y","Dead","TB",
                "Switches","Crs_x","CK","Fouls","Fouls Drawn","Penalty Kicks Won","PKcon","Recoveries","Won",
                "Aerial Duel Success Rate","Tackles","TklW_y","Def 3rd","Mid 3rd","Att 3rd","Int_y","Tkl+Int","Clr","Err","Tackle Success Rate","League"]]
    
    dat = dat.rename(columns={"Progressive Passes Received_x":"Progressive Passes Received","PrgDist_x":"Progressive Carrying Distance",
                               "PrgDist_y":"Progressive Passing Distance","Cmp.1":"Short Passes Completed","Att.1":"Short Passes Attempted",
                               "Cmp%.1":"Short Pass Completion %", "Cmp.2":"Medium Passes Completed","Att.2":"Medium Passes Attempted",
                               "Cmp%.2":"Medium Pass Completion %","Cmp.3":"Long Passes Completed","Att.3":"Long Passes Attempted",
                               "Cmp%.3":"Long Pass Completion %","Live_y":"Live Ball Passes","Dead":"Dead Ball Passes","TB":"Through Balls",
                               "Crs_x":"Crosses","CK":"Corner Kicks","TklW_y":"Tackles Won","Def 3rd":"Defensive 3rd Tackles",
                               "Mid 3rd":"Middle 3rd Tackles","Att 3rd":"Attacking 3rd Tackles","Int_y":"Interceptions","Tkl+Int":"Tackles + Interceptions",
                               "Clr":"Clearances","Err":"Errors Leading to a Shot"})
    
    print(dat.columns)
    return dat
    
    
def comparison_radar(rdat,player_1,player_2):
    """
    Plots a radar chart comparing two players.

    Args:
        rdat = Dataframe containing the variables to be plotted. Must include "Player" and "Squad".\n  
        player_1 = Player on the chart. Selected from the selectbox provided.\n  
        player_2 = Player on the chart. Selected from the selecttbox provided.  

    Returns:
        Comparative radar chart displaying two players' characteristics, as well as their names and the club they play for.

    """
    params = list(rdat.columns)
    params = params[2:]

    ranges =  []
    for x in params:
        a = min(rdat[params][x])
        a = a - (a*0.25)

        b = max(rdat[params][x])
        b = b + (b*0.25)
        ranges.append((a,b))

    a_values = rdat[rdat["Player"]==player_1].iloc[0].values[2:].tolist()
    b_values = rdat[rdat["Player"]==player_2].iloc[0].values[2:].tolist()
    values = [a_values, b_values]
    a_team = rdat[rdat["Player"]==player_1]["Squad"].values[0]
    b_team = rdat[rdat["Player"]==player_2]["Squad"].values[0]
    print(a_team)
    print(b_team)

    title = dict(
        title_name = player_1,
        title_color="red",
        subtitle_name =a_team,
        subtitle_color = "red",
        title_name_2=player_2,
        title_color_2="blue",
        subtitle_name_2=b_team,
        subtitle_color_2 = "blue",
        title_fontsize = 18,
        subtitle_fontsize=15
    )

    endnote = "Data Courtesy of FBref. All stats are presented per 90 minutes played."

    radar = Radar()

    fig,ax = radar.plot_radar(ranges=ranges, params=params, values=values, radar_color=['red','blue'],title=title, endnote = endnote,compare=True)

    st.pyplot(fig)






