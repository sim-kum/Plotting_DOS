import pyprocar
pyprocar.dosplot(
                  mode='stack',
                  colors=['lawngreen','darkgreen', 'orangered', 'cyan','royalblue'],
                  items=dict(In=[1, 2, 3], Sn=[1,2,3],O=[1, 2, 3] , H=[0], Pt=[4, 5, 6, 7,8]),
                  orientation='horizontal',
                  elimit=[-4, 4],
                  vmax = 150,
                  plot_total=False,
                  savefig = 'monomer.png')
