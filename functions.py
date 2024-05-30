import pandas as pd



def clean_standard(std):
    std.rename(columns={"Gls":"Goals Scored", "Ast":"Assists","G+A":"Goals + Assists","Min":"Minutes Played", "xG":"Expected Goals","xAG":"Expected Assists","PK":"Penalties Scored","PKatt":"Penalties Attempted","CrdY":"Yellow Cards", "CrdR":"Red Cards",
                         "PrgC":"Progressive Carries","PrgP":"Progressive Passes","PrgR":"Progressive Passes Received", "G-PK":"Non-Penalty Goals",
                          "npxG":"Non-Penalty Expected Goals", }, inplace=True)
    return std

def clean_poss(poss):
    poss.rename(columns={"Att 3rd":"Touches in the Attacking Third", "TotDist":"Total Carry Distance","Att":"Dribbles Attempted", "Succ%":"Dribble Success %",
                         "1/3":"Carries Into the Final Third", "CPA":"Carries into the Penalty Area","Rec":"Passes Received",
                         "PrgR":"Progressive Passes Received","Def Pen":"Touches in the Defensive Penalty Area",
                         "Def 3rd":"Defensive 1/3 Touches","Mid 3rd":"Middle 1/3 Touches","Att Pen":"Attacking Penalty Area Touches",},inplace=True)
    poss.drop(columns=["Pos","Age","Born","90s","Nation","Matches"], inplace=True)
    return poss

def clean_pass(pas):
    pas.rename(columns={"KP":"Key Passes","CrsPA":"Crosses into the Penalty Area","PPA":"Passes into the Penalty Area",
                        "A-xAG":"Assists Overperformance","Att":"Passes Attempted",
                        "Cmp%":"Pass Completion %"},inplace=True)
    pas.drop(columns=["Pos","Age","Born","90s","Nation","Matches"], inplace=True)
    return pas

def clean_ptypes(ptype):
    ptype.rename(columns={"Sw":"Switches"},inplace=True)
    ptype.drop(columns=["Pos","Age","Born","90s","Nation","Att","Matches"], inplace=True)
    return ptype

def clean_misc(misc):
    misc.rename(columns={"Recov":"Recoveries","Won%":"Aerial Duel Success Rate","Fls":"Fouls", "'Int":"Interceptions", "Fld":"Fouls Drawn","PKwon":"Penalty Kicks Won"}, inplace=True)
    misc.drop(columns=["Pos","Age","Born","90s","Nation","Matches"], inplace=True)
    return misc
    
def clean_def_actions(defe):
    defe.rename(columns={"Tkl":"Tackles"},inplace=True)
    defe.drop(columns=["Pos","Age","Born","90s","Nation","Matches"], inplace=True)
    defe['Tackle Success Rate'] = (defe['TklW']/defe["Tackles"]) * 100
    return defe


def merge_stats(league, std, poss, pas, ptype, misc, defe):
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
    data = pd.concat([pl,li], axis=0)
    print(data["League"].unique())
    return data

def scatter_variables(data):    # Variables to appear on the x,y scatterplot
    dat = data[["Player","Goals Scored","Assists","Goals + Assists", "Non-Penalty Goals","Penalties Scored","Penalties Attempted",
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
    
    




#file = "pl.xlsx"
#pl.to_excel(file, index=False)


