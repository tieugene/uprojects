# -*- coding: utf-8 -*-
'''
treeselect.py - stuff to select item from tree-like list.
'''

from PyQt4 import QtCore, QtGui

class	Node:
	def	__init__(self, parentNode = None, s1 = None ):
		self.parent	= parentNode
		self.str1		= s1
		self.children	= []

class	TreeModel(QtCore.QAbstractItemModel):
	def	__init__(self, parent = None):
		QtCore.QAbstractItemModel.__init__(self, parent)
		self.rootNode = 0

	def	index(self, row, column, parent):
		if (self.rootNode):
			parentNode = self.nodeFromIndex(parent)
			if (parentNode):
				return self.createIndex(row, column, parentNode.children[row])
		return QtCore.QModelIndex()

	def	hasChildren(self, parent):
		parentNode = self.nodeFromIndex(parent)
		if (not parentNode):
			return False
		else:
			return (len(parentNode.children) > 0)

	def	parent(self, index):
		node = self.nodeFromIndex(index)
		if (not node):
			return QtCore.QModelIndex()
		parentNode = node.parent
		if (not parentNode):
			return QtCore.QModelIndex()
		grandparentNode = parentNode.parent
		if (not grandparentNode):
			return QtCore.QModelIndex()
		row = grandparentNode.children.index(parentNode)
		return self.createIndex(row, index.column(), parentNode)

	def	rowCount(self, index):
		node = self.nodeFromIndex(index)
		if ( node ):
			return len(node.children)
		else:
			return 0

	def	columnCount(self, index):
		return 1;

	def	data(self, index, role):
		col = index.column()
		node = self.nodeFromIndex(index)
		if ((role == QtCore.Qt.DisplayRole) and (node) and (col == 0)):
			return QtCore.QVariant(node.str1)
		return QtCore.QVariant()

	def	setRootNode(self, node):
		self.rootNode = node
		self.reset()

	def	nodeFromIndex(self, index):
		if (index.isValid()):
			return (index.internalPointer())
		else:
			return self.rootNode

	def	flags(self, index):
		if ( index.isValid() ):
			return (QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
		else:
			return 0

	def	headerData(self, section, orientation, role):
		if (orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole and section == 0):
			    return QtCore.QVariant(QtGui.QApplication.translate("mxattr", "Number"))
		return QtCore.QVariant()

class	TreeSelectDialog(QtGui.QDialog):
	def	__init__(self, parent = None):
		QtGui.QDialog.__init__(self, parent)
		#self.resize(QtCore.QSize(QtCore.QRect(0,0,315,300).size()).expandedTo(self.minimumSizeHint()))
		self.vbl = QtGui.QVBoxLayout(self)
		self.model = TreeModel()
		self.tree = QtGui.QTreeView(self)
		self.tree.setModel(self.model)
		self.tree.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
		self.tree.setSelectionBehavior(QtGui.QAbstractItemView.SelectItems)
		self.tree.setExpandsOnDoubleClick(False)
		self.tree.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
		self.vbl.addWidget(self.tree)
		self.buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Close, QtCore.Qt.Horizontal, self)
		self.vbl.addWidget(self.buttonBox)
		QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), self.accept)
		QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), self.reject)

	def	__r(self, a, nlist):
		for n in nlist:
			tn = type(n).__name__
			if (tn == 'str'):
				a.children.append(Node(a, n))
			elif (tn == 'dict'):
				n1 = n.keys()[0]
				a1 = Node(a, n1)
				a.children.append(a1)
				self.__r(a1, n[n1])
			else:
				print "error"

	def	_letsGo(self, tree = None):
		retvalue = ""
		root = Node()
		self.__r(root, tree)
		self.model.setRootNode(root)
		self.tree.expandAll()
		self.tree.header().setStretchLastSection(True)
		self.tree.resizeColumnToContents(1)
		if (self.exec_()):	# accepted
			n = self.model.nodeFromIndex(self.tree.currentIndex())
			while (n and n.parent):	# root is Node too
				retvalue = "/" + n.str1 + retvalue
				n = n.parent
		return retvalue
