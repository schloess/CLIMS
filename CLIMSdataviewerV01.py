#####~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#####
##### CLIMS data viewer V01 - FS - 01/30/2019 
##### Please define the default search path and experiment name below
##### for an enhanced user experience!
#####~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#####
##### DEFAULT SEARCH PATH:
DPATH='/Volumes/Chunky/LOVECLIP/LOVECLIM1.3/'
##### DEFAULT EXPERIMENT NAME
DNAME='pivar02'
#####~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#####
#####~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#####
import dash
import dash_core_components as dcc
import dash_html_components as html

from netCDF4 import Dataset
import numpy as np
import plotly.graph_objs as go

#import json
import os
import os.path

#from mpl_toolkits.basemap import Basemap
#####~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#####
#####
#####  COMPARE TWO EXPERIMENTS OR SNAPSHOTS:
#####
#####~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#####
## GET LIST OF EXPERIMENTS
#DEFAULT
all_experiments=os.listdir(DPATH)
nnnn=0
for n in range(len(all_experiments)):
    if not os.path.isdir(DPATH+all_experiments[n-nnnn]+'/output'):
        all_experiments.remove(all_experiments[n-nnnn])
        nnnn+=1
#####~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#####


#####~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#####
### APP:
available_variables=['SAT', 'Total precipitation']

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
################################################################################################################    
# HEADER
    html.Div(
        html.H1(
            id='app-headline',
            children='CLIMS data viewer'
        ),
        style={'width': '72%','display': 'inline-block','verticalAlign':'middle'}
    ),
    html.Div(
        html.Div(
            id='delta-n-text',
            children=' Deln:'
        ),
        style={'width': '10%','display': 'inline-block','verticalAlign':'bottom'}
    ),
     html.Div(
        html.Div(
            id='factor-n-text',
            children=' Chunkl:'
        ),
        style={'width': '15%','display': 'inline-block','verticalAlign':'bottom'}
    ),    
################################################################################################################    
# DATASET 1
    html.Div(
        dcc.Input(
            id='data--path1',
            value='/Volumes/Chunky/LOVECLIP/LOVECLIM1.3/',
            type='text',
            size=60,
            debounce=True
        ),
        style={'width': '39%','display': 'inline-block','verticalAlign':'middle'}
    ),   
    html.Div(
        dcc.Dropdown(
            id='drop--experiment1',
            #options=[{'label': i, 'value': i} for i in all_experiments],
            value=DNAME,
            clearable=False

        ),    
        style={'width': '29%','display': 'inline-block','verticalAlign':'middle'}
    ),
    html.Div(
        html.Div(
            id='delta-n1',
            children=' '
        ),
        style={'width': '4%','display': 'inline-block','verticalAlign':'middle'}
    ),
    html.Div(
        dcc.Input(
            id='input-n1',
            value=0,
            type='text',
            size=5,
            debounce=True
        ),
        style={'width': '6%','display': 'inline-block','verticalAlign':'middle'}
    ),
    html.Div(
        html.Div(
            id='factor-n1',
            children=' '
        ),
        style={'width': '4%','display': 'inline-block','verticalAlign':'middle'}
    ),
    html.Div(
        dcc.Input(
            id='infac-n1',
            value=1,
            type='text',
            size=5,
            debounce=True
        ),
        style={'width': '9%','display': 'inline-block','verticalAlign':'middle'}
    ),
################################################################################################################    
# DATASET 2
    html.Div(
        dcc.Input(
            id='data--path2',
            value='/Volumes/Chunky/LOVECLIP/LOVECLIM1.3/',
            type='text',
            size=60,
            debounce=True
        ),
        style={'width': '39%','display': 'inline-block','verticalAlign':'middle'}
    ),    
    html.Div(
        dcc.Dropdown(
            id='drop--experiment2',
            #options=[{'label': i, 'value': i} for i in all_experiments],
            value=DNAME,
            clearable=False
        ),
        style={'width': '29%','display': 'inline-block','verticalAlign':'middle'}
    ),
    html.Div(
        html.Div(
            id='delta-n2',
            children=' '
        ),
        style={'width': '4%','display': 'inline-block','verticalAlign':'middle'}
    ),
    html.Div(
        dcc.Input(
            id='input-n2',
            value=0,
            type='text',
            size=5,
            debounce=True
        ),
        style={'width': '6%','display': 'inline-block','verticalAlign':'middle'}
        ),
    html.Div(
        html.Div(
            id='factor-n2',
            children=''
        ),
        style={'width': '4%','display': 'inline-block','verticalAlign':'middle'}
    ),
    html.Div(
        dcc.Input(
            id='infac-n2',
            value=1,
            type='text',
            size=5,
            debounce=True
        ),
        style={'width': '9%','display': 'inline-block','verticalAlign':'middle'}
    ),
################################################################################################################    
# STORAGE    
    #dcc.Store(id='experiment-list'), 
    dcc.Store(id='data--exp1'),
    dcc.Store(id='data--exp2'),          
    dcc.Store(id='exp--icevol1'),
    dcc.Store(id='exp--icevol2'),    

################################################################################################################    
# CHUNK SLIDER AND ICEVOLUME        
    dcc.Slider(
        id='chunk--slider',
        min=0,
        value=0,
        step=1
    ),
    dcc.Graph(id='icevol--plot'),
################################################################################################################    
# CONTOUR PLOTS    
    html.Div(
        dcc.Dropdown(
            id='drop--difference',
            value=0,
            clearable=False
        ),
        style={'width': '14%','display': 'inline-block','verticalAlign':'middle'}
    ),    
    html.Div(    
        html.Button(id='submit-to-plots', n_clicks=0, children='Update'),
        style={'display': 'inline-block','width': '9%','verticalAlign':'middle'}
    ),
    html.Div(
        html.Div(id='plot--state'),
        style={'width': '74%','display': 'inline-block','verticalAlign':'middle'}
    ),    
    html.Div(
        dcc.Graph(id='NH--plot'),
        style={'width': '59%', 'display': 'inline-block'}
    ),
    html.Div(
        dcc.Graph(id='AIS--plot'),
        style={'width': '39%', 'display': 'inline-block'}
    )                  
])

#########################################################################
##
##   GET PATH OF EXPERIMENTS
##
#########################################################################
### get experiment lists and update dropdown
@app.callback(
    dash.dependencies.Output('drop--experiment1', 'options'), 
    [dash.dependencies.Input('data--path1','value')])
def get_all_experiments1(datapath):
    expnames=os.listdir(datapath)
    nnn=0
    for n in range(len(expnames)):
        if not os.path.isdir(datapath+expnames[n-nnn]+'/output'):
            expnames.remove(expnames[n-nnn])
            nnn+=1 
    return [{'label': i, 'value': i} for i in expnames] 
@app.callback(
    dash.dependencies.Output('drop--experiment2', 'options'), 
    [dash.dependencies.Input('data--path2','value')])
def get_all_experiments2(datapath):
    expnames=os.listdir(datapath)
    nnn=0
    for n in range(len(expnames)):
        if not os.path.isdir(datapath+expnames[n-nnn]+'/output'):
            expnames.remove(expnames[n-nnn])
            nnn+=1 
    return [{'label': i, 'value': i} for i in expnames]
### get experiment path:
@app.callback(
    dash.dependencies.Output('data--exp1', 'data'), 
    [dash.dependencies.Input('data--path1','value'),
     dash.dependencies.Input('drop--experiment1','value')
     ])
def get_experiments1(datapath,expname):
    exppath=datapath+expname
    return exppath
@app.callback(
    dash.dependencies.Output('data--exp2', 'data'), 
    [dash.dependencies.Input('data--path2','value'),
     dash.dependencies.Input('drop--experiment2','value')
     ])
def get_experiments2(datapath,expname):
    exppath=datapath+expname
    return exppath
@app.callback(
    dash.dependencies.Output('drop--difference','options'), 
    [dash.dependencies.Input('drop--experiment1','value'),
     dash.dependencies.Input('drop--experiment2','value')])
def get_plot_type(input1,input2):
    myoptions=['difference',input1,input2]
    #print myoptions
    theoptions=[{'label': myoptions[i], 'value': i} for i in range(len(myoptions))]
    #print theoptions
    return theoptions
#########################################################################
##
##   SOME RESETS: 
##
######################################################################### 
@app.callback(
    dash.dependencies.Output('chunk--slider','value'),
    [dash.dependencies.Input('data--exp1','data'),
     dash.dependencies.Input('data--exp2','data'),
     dash.dependencies.Input('input-n1','value'),
     dash.dependencies.Input('input-n2','value'),
     dash.dependencies.Input('infac-n1','value'),
     dash.dependencies.Input('infac-n2','value'),      
     dash.dependencies.Input('drop--difference','value')
    ])
def reset_the_slider(x0,x1,x2,x3,x4,x5,x6):
    return 0


#########################################################################
##
##   PLOT ICE VOLUME AND GET CHUNKS 
##
######################################################################### 
# get icevolumes:    
@app.callback(
    dash.dependencies.Output('exp--icevol1','data'),
    [dash.dependencies.Input('data--exp1', 'data')])
def get_exp_props1(expname):
    #get time series of icevol in SL equivalent:
    iv=-0.9/3.6e14*(np.loadtxt(expname+'/output/icevol.dat')[:,1]-3.0e16)
    data = {'yy' : np.squeeze(iv)}
    data['xx']=np.squeeze(np.arange(len(iv))) 
    return data
@app.callback(
    dash.dependencies.Output('exp--icevol2','data'),
    [dash.dependencies.Input('data--exp2', 'data')])    
def get_exp_props2(expname):
    #get time series of icevol in SL equivalent:
    iv=-0.9/3.6e14*(np.loadtxt(expname+'/output/icevol.dat')[:,1]-3.0e16)
    data = {'yy' : np.squeeze(iv)}
    data['xx']=np.squeeze(np.arange(len(iv))) 
    return data
@app.callback(
    dash.dependencies.Output('chunk--slider','max'),
    [dash.dependencies.Input('data--exp1','data'),
     dash.dependencies.Input('data--exp2','data'),
     dash.dependencies.Input('input-n1','value'),
     dash.dependencies.Input('input-n2','value'),
     dash.dependencies.Input('infac-n1','value'),
     dash.dependencies.Input('infac-n2','value'),     
     dash.dependencies.Input('drop--difference','value')
    ])
# adjust the chunk slider:    
def no_of_chunks_experiment(expname1,expname2,ntext1,ntext2,nfactext1,nfactext2,pltype):
    if pltype==0 or pltype==1:
        PNHPATH=expname1+'/output/psuim_nh/'
        chunk_dirs=os.listdir(PNHPATH)
        nn=0
        for n in range(len(chunk_dirs)):
            if not os.path.isfile(PNHPATH+chunk_dirs[n-nn]+'/fort.92.nc'):
                chunk_dirs.remove(chunk_dirs[n-nn])
                nn+=1
        NCHUNKSall=len(chunk_dirs)
    if pltype==0 or pltype==2:     
        PNHPATH=expname2+'/output/psuim_nh/'
        chunk_dirs=os.listdir(PNHPATH)
        nn=0
        for n in range(len(chunk_dirs)):
            if not os.path.isfile(PNHPATH+chunk_dirs[n-nn]+'/fort.92.nc'):
                chunk_dirs.remove(chunk_dirs[n-nn])
                nn+=1
        NCHUNKS2all=len(chunk_dirs) 
    nskip1=int(ntext1)
    nskip2=int(ntext2)
    nskip=nskip2-nskip1
    nfac1=int(nfactext1)
    nfac2=int(nfactext2)
    if pltype==0:
        if nfac1==nfac2:
            NCHUNKS=NCHUNKSall
            NCHUNKS2=NCHUNKS2all
        else:
            # this assumes that either nfac1/nfac2 or nfac2/nfac1 is an integer
            if nfac1>nfac2:
                nfacn=nfac1/nfac2
                NCHUNKS=NCHUNKSall
                NCHUNKS2=NCHUNKS2all/nfacn         
            else:
                nfacn=nfac2/nfac1    
                NCHUNKS=NCHUNKSall/nfacn
                NCHUNKS2=NCHUNKS2all              
        nmaxsl=min(NCHUNKS-max(nskip,0)/nfac1,NCHUNKS2-max(-nskip,0)/nfac2) 
        nmaxsl=max(0,nmaxsl)
    elif pltype==1:
        nmaxsl=NCHUNKSall       
    elif pltype==2:
        nmaxsl=NCHUNKS2all  
    return nmaxsl
# renew icevolume plot
@app.callback(
    dash.dependencies.Output('icevol--plot', 'figure'),
    [dash.dependencies.Input('exp--icevol1', 'data'),
     dash.dependencies.Input('exp--icevol2', 'data'),
     dash.dependencies.Input('input-n1','value'),
     dash.dependencies.Input('input-n2','value'),
     dash.dependencies.Input('infac-n1','value'),
     dash.dependencies.Input('infac-n2','value'), 
     dash.dependencies.Input('chunk--slider', 'value'),
     dash.dependencies.Input('drop--difference','value')     
    ])
def update_sealev(datain1,datain2,ntext1,ntext2,nfactext1,nfactext2,nstep,pltype):
    nskip1=int(ntext1)
    nskip2=int(ntext2)
    nskip=nskip2-nskip1
    nfac1=int(nfactext1)
    nfac2=int(nfactext2)
    for n in range(len(datain2['xx'])):
        datain2['xx'][n]=datain2['xx'][n]*nfac2+nskip2

    for n in range(len(datain1['xx'])):
        datain1['xx'][n]=datain1['xx'][n]*nfac1+nskip1
    trace0 = go.Scatter(
        x = datain1['xx'],
        y = datain1['yy'],
        mode = 'lines',
        name = 'ice volume',
        showlegend=False
    )
    trace1 = go.Scatter(
        x = datain2['xx'],
        y = datain2['yy'],
        mode = 'lines',
        name = 'ice volume',
        showlegend=False
    )
    if pltype==0:
        xdum=max(nskip1,nskip2)+max(nfac1,nfac2)*nstep
        xpo=[xdum,xdum]
        ndum1=nstep*max(1,nfac2/nfac1)+max(nskip2-nskip1,0)/nfac1
        ndum2=nstep*max(1,nfac1/nfac2)+max(nskip1-nskip2,0)/nfac2
        ypo=[datain1['yy'][ndum1],datain2['yy'][ndum2]] 
    elif pltype==1:
        xpo=[nstep*nfac1+nskip1]
        ypo=[datain1['yy'][nstep]] 
    elif pltype==2:
        xpo=[nstep*nfac2+nskip2]
        ypo=[datain2['yy'][nstep]]                      
    trace2 = go.Scatter(
        x = xpo,
        y = ypo,
        mode = 'markers',
        marker = {'size': 15},
        showlegend=False
    )
    data = [trace0, trace1, trace2]
    return {
        'data': data,
        'layout': go.Layout(
            yaxis={
                'title': 'ice volume [SLE]'
            },
            height=200,
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }

@app.callback(dash.dependencies.Output('plot--state', 'children'),
              [dash.dependencies.Input('submit-to-plots', 'n_clicks')],
              [dash.dependencies.State('chunk--slider', 'value'),
               dash.dependencies.State('input-n1','value'),              
               dash.dependencies.State('drop--experiment1', 'value'),
               dash.dependencies.State('drop--experiment2', 'value'),
               dash.dependencies.State('drop--difference','value')])
def update_output(n_clicks, nchunkin, nskiptext,ename1,ename2,pltype):
    nskipin=int(nskiptext)
    #print nskipin
    if nskipin>0:
        ne1=nchunkin+nskipin
        ne2=nchunkin
    elif nskipin<=0:
        ne1=nchunkin
        ne2=nchunkin-nskipin
        #print ne1
        #print ne2
    if pltype==0:
        textout='Chunk '+str(ne1)+' of '+ename1+' minus Chunk '+str(ne2)+' of '+ename2 
    elif pltype==1:
        textout='Chunk '+str(ne1)+' of '+ename1
    elif pltype==2:
        textout='Chunk '+str(ne2)+' of '+ename2           
    return u'''
        Showing {}
    '''.format(textout)
#########################################################################
##
##   PRODUCE NH CONTOUR PLOT
##
#########################################################################    
@app.callback(dash.dependencies.Output('NH--plot', 'figure'),
              [dash.dependencies.Input('submit-to-plots', 'n_clicks')],
              [dash.dependencies.State('chunk--slider', 'value'),
               dash.dependencies.State('input-n1','value'),
               dash.dependencies.State('drop--experiment1', 'value'),
               dash.dependencies.State('drop--experiment2', 'value'), 
               dash.dependencies.State('data--path1','value'),
               dash.dependencies.State('drop--difference','value')])
def update_NH(n_clicks, nchunkin,nskiptext, ename1,ename2,datapath,pltype):
    nskipin=int(nskiptext)
    if nskipin>0:
        ne1=nchunkin+nskipin
        ne2=nchunkin
    elif nskipin<=0:
        ne1=nchunkin
        ne2=nchunkin-nskipin
    if pltype==0:                    
        PNHPATH=datapath+ename1+'/output/psuim_nh/'
        chunk_dirs=os.listdir(PNHPATH)
        nn=0
        for n in range(len(chunk_dirs)):
            if not os.path.isfile(PNHPATH+chunk_dirs[n-nn]+'/fort.92.nc'):
                chunk_dirs.remove(chunk_dirs[n-nn])
                nn+=1
        DFILE=PNHPATH+chunk_dirs[ne1]+'/fort.92.nc'
        ff  = Dataset(DFILE , mode='r')
        h= ff.variables['h']
        lat= ff.variables['lat'][:]
        lon= ff.variables['lon'][:]
        wmask = ff.variables['maskwater'] 
        lmask1=np.squeeze(wmask[0,:,:])    
        hsh1=np.squeeze(h[0,:,:])
        ff.close()
        PNHPATH=datapath+ename2+'/output/psuim_nh/'
        chunk_dirs=os.listdir(PNHPATH)
        nn=0
        for n in range(len(chunk_dirs)):
            if not os.path.isfile(PNHPATH+chunk_dirs[n-nn]+'/fort.92.nc'):
                chunk_dirs.remove(chunk_dirs[n-nn])
                nn+=1
        DFILE=PNHPATH+chunk_dirs[ne2]+'/fort.92.nc'
        ff  = Dataset(DFILE , mode='r')
        h= ff.variables['h']
        wmask = ff.variables['maskwater'] 
        lmask2=np.squeeze(wmask[0,:,:])    
        hsh2=np.squeeze(h[0,:,:])
        ff.close()
        hdif=hsh1-hsh2
        cscale=np.amax(np.abs(hdif))
        hdif[np.abs(hdif)<0.00001]=np.nan
        trace0= go.Contour(
            x=lon,
            y=lat,
            z=hdif,
            zmin=-cscale,
            zmax=cscale,
            colorscale='RdBu',
            contours={'showlines':False},
            colorbar={
                'yanchor':'middle',
                'lenmode':'fraction',
                'len':0.7
            }    
        )
        trace1= go.Contour(
            x=lon,
            y=lat,
            z=lmask1,
            ncontours=2,
            contours={
                'coloring':'none'},
            line={
                'color':'lightgray',
                'smoothing':1.3,
                'width':2}
        )
        trace2= go.Contour(
            x=lon,
            y=lat,
            z=lmask2,
            ncontours=2,
            contours={
                'coloring':'none'},
            line={
                'color':'black',
                'smoothing':1.3,
                'width':2}
        )
    else:
        if pltype==1:
            ename=ename1
            ne=ne1
        else:
            ename=ename2
            ne=ne2
        PNHPATH=datapath+ename+'/output/psuim_nh/'
        chunk_dirs=os.listdir(PNHPATH)
        nn=0
        for n in range(len(chunk_dirs)):
            if not os.path.isfile(PNHPATH+chunk_dirs[n-nn]+'/fort.92.nc'):
                chunk_dirs.remove(chunk_dirs[n-nn])
                nn+=1
        DFILE=PNHPATH+chunk_dirs[ne]+'/fort.92.nc'
        ff  = Dataset(DFILE , mode='r')
        h= ff.variables['h']
        lat= ff.variables['lat'][:]
        lon= ff.variables['lon'][:]
        wmask = ff.variables['maskwater'] 
        lmask=np.squeeze(wmask[0,:,:])    
        hsh=np.squeeze(h[0,:,:])
        ff.close()
        hsh[hsh<100.0]=np.nan                    
        hsland=np.copy(hsh)
        hsland[lmask==1.0]=np.nan
        hsh[lmask==0.0]=np.nan
        trace0= go.Contour(
            x=lon,
            y=lat,
            z=hsland,
            colorscale='YlGnBu',
            contours={'showlines':False},
            colorbar={
                'yanchor':'bottom',
                'lenmode':'fraction',
                'len':0.45
            }    
        )
        trace1=go.Contour(
            x=lon,
            y=lat,
            z=hsh,
            colorscale='YlOrRd',
            colorbar={
                'yanchor':'top',
                'lenmode':'fraction',
                'len':0.45
            },         
            contours={'showlines':False}
        )    
        trace2=go.Contour(
            x=lon,
            y=lat,
            z=lmask,
            ncontours=2,
            contours={
                'coloring':'none'},
            line={
                'color':'lightgray',
                'smoothing':1.3,
                'width':2}
        )    
    data = [trace0,trace1,trace2]
    return {
        'data':data,
        'layout':go.Layout(
            title='Northern Hemisphere Ice Thickness',
            xaxis={'showgrid':False,
                   'zeroline':False},
            yaxis={'showgrid':False,
                   'zeroline':False},
            width=1000,
            height=500
        )
    }
#########################################################################
##
##   PRODUCE SH CONTOUR PLOT
##
#########################################################################
@app.callback(dash.dependencies.Output('AIS--plot', 'figure'),
              [dash.dependencies.Input('submit-to-plots', 'n_clicks')],
              [dash.dependencies.State('chunk--slider', 'value'),
               dash.dependencies.State('input-n1','value'),
               dash.dependencies.State('drop--experiment1', 'value'),
               dash.dependencies.State('drop--experiment2', 'value'), 
               dash.dependencies.State('data--path1','value'),
               dash.dependencies.State('drop--difference','value')])
def update_SH(n_clicks, nchunkin,nskiptext, ename1,ename2,datapath,pltype):
    nskipin=int(nskiptext)
    if nskipin>0:
        ne1=nchunkin
        ne2=nchunkin-nskipin
    elif nskipin<=0:
        ne1=nchunkin+nskipin
        ne2=nchunkin
    if pltype==0:                    
        PNHPATH=datapath+ename1+'/output/psuim_sh/'
        chunk_dirs=os.listdir(PNHPATH)
        nn=0
        for n in range(len(chunk_dirs)):
            if not os.path.isfile(PNHPATH+chunk_dirs[n-nn]+'/fort.92.nc'):
                chunk_dirs.remove(chunk_dirs[n-nn])
                nn+=1
        DFILE=PNHPATH+chunk_dirs[ne1]+'/fort.92.nc'
        ff  = Dataset(DFILE , mode='r')
        h= ff.variables['h']
        wmask = ff.variables['maskwater'] 
        lmask1=np.squeeze(wmask[0,:,:])    
        hsh1=np.squeeze(h[0,:,:])
        ff.close()
        PNHPATH=datapath+ename2+'/output/psuim_sh/'
        chunk_dirs=os.listdir(PNHPATH)
        nn=0
        for n in range(len(chunk_dirs)):
            if not os.path.isfile(PNHPATH+chunk_dirs[n-nn]+'/fort.92.nc'):
                chunk_dirs.remove(chunk_dirs[n-nn])
                nn+=1
        DFILE=PNHPATH+chunk_dirs[ne2]+'/fort.92.nc'
        ff  = Dataset(DFILE , mode='r')
        h= ff.variables['h']
        wmask = ff.variables['maskwater'] 
        lmask2=np.squeeze(wmask[0,:,:])    
        hsh2=np.squeeze(h[0,:,:])
        ff.close()
        hdif=hsh1-hsh2
        cscale=np.amax(np.abs(hdif))
        hdif[np.abs(hdif)<0.00001]=np.nan
        trace0= go.Contour(
            z=hdif,
            zmin=-cscale,
            zmax=cscale,
            colorscale='RdBu',
            contours={'showlines':False},
            colorbar={
                'yanchor':'middle',
                'lenmode':'fraction',
                'len':0.7
            }    
        )
        trace1= go.Contour(
            z=lmask1,
            ncontours=2,
            contours={
                'coloring':'none'},
            line={
                'color':'lightgray',
                'smoothing':1.3,
                'width':2}
        )
        trace2= go.Contour(
            z=lmask2,
            ncontours=2,
            contours={
                'coloring':'none'},
            line={
                'color':'black',
                'smoothing':1.3,
                'width':2}
        )
    else:
        if pltype==1:
            ename=ename1
            ne=ne1
        else:
            ename=ename2
            ne=ne2
        PNHPATH=datapath+ename+'/output/psuim_sh/'
        chunk_dirs=os.listdir(PNHPATH)
        nn=0
        for n in range(len(chunk_dirs)):
            if not os.path.isfile(PNHPATH+chunk_dirs[n-nn]+'/fort.92.nc'):
                chunk_dirs.remove(chunk_dirs[n-nn])
                nn+=1
        DFILE=PNHPATH+chunk_dirs[ne]+'/fort.92.nc'
        ff  = Dataset(DFILE , mode='r')
        h= ff.variables['h']
        wmask = ff.variables['maskwater'] 
        lmask=np.squeeze(wmask[0,:,:])    
        hsh=np.squeeze(h[0,:,:])
        ff.close()
        hsh[hsh<100.0]=np.nan                    
        hsland=np.copy(hsh)
        hsland[lmask==1.0]=np.nan
        hsh[lmask==0.0]=np.nan
        trace0= go.Contour(
            z=hsland,
            colorscale='YlGnBu',
            contours={'showlines':False},
            colorbar={
                'yanchor':'bottom',
                'lenmode':'fraction',
                'len':0.45
            }    
        )
        trace1=go.Contour(
            z=hsh,
            colorscale='YlOrRd',
            colorbar={
                'yanchor':'top',
                'lenmode':'fraction',
                'len':0.45
            },         
            contours={'showlines':False}
        )    
        trace2=go.Contour(
            z=lmask,
            ncontours=2,
            contours={
                'coloring':'none'},
            line={
                'color':'lightgray',
                'smoothing':1.3,
                'width':2}
        )  
    data = [trace0,trace1,trace2]
    return {
        'data':data,
        'layout':go.Layout(
            title='Antarctic Ice Thickness',
            xaxis={'showgrid':False,
                   'zeroline':False},
            yaxis={'showgrid':False,
                   'zeroline':False},
            width=550,
            height=500       
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)



