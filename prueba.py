from graphviz import Digraph

dotGR = Digraph('Reporte Gramatical',filename='Grmatical ASC')

dotGR.node('init','init')
dotGR.node('instrucciones','instrucciones')
dotGR.edge('init','instrucciones')
dotGR.view()