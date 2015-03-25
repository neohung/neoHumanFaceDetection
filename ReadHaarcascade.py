import xml.etree.ElementTree as ET
from decimal import Decimal
class cascade(object):
    def __init__(self):
        super (cascade, self).__init__ ()

class readXml(object):
     def __init__(self, xmlfilename):
        self.stage = []
        tree = ET.ElementTree(file=xmlfilename)
        for elem in tree.iter(tag='size'):
            tmp = elem.text
            size=tmp.split(" ")
        self.width = int(size[0])
        self.height = int(size[1])
        stage_i=0
        for stages in tree.iter(tag='stages'):
            for stages_ in stages:
                x = cascade()
                self.stage.append(x)
                for stage_threshold in stages_.iter(tag='stage_threshold'):
                    self.stage[stage_i].stage_threshold = Decimal(stage_threshold.text)
                    #print "s"+str(stage_i)+") stage_threshold: "+ stage_threshold.text
                for parent in stages_.iter(tag='parent'):
                    self.stage[stage_i].parent = Decimal(parent.text)
                    #print "s"+str(stage_i)+") parent: "+ parent.text
                for next in stages_.iter(tag='next'):
                    self.stage[stage_i].next = Decimal(next.text)
                    #print "s"+str(stage_i)+") next: "+ next.text
                for trees in stages_.iter(tag='trees'):
                    tree_i=0
                    self.stage[stage_i].tree = []
                    for trees_ in trees:
                        for trees__ in trees_:
                            y = cascade()
                            self.stage[stage_i].tree.append(y)
                            for threshold in trees__.iter(tag='threshold'):
                                self.stage[stage_i].tree[tree_i].threshold = Decimal(threshold.text)
                                #print "s"+str(stage_i)+",t"+str(tree_i)+") threshold: "+ threshold.text
                            for left_val in trees__.iter(tag='left_val'):
                                self.stage[stage_i].tree[tree_i].left_val = Decimal(left_val.text)
                                #print "s"+str(stage_i)+",t"+str(tree_i)+") left_val: "+ left_val.text
                            for right_val in trees__.iter(tag='right_val'):
                                self.stage[stage_i].tree[tree_i].right_val = Decimal(right_val.text)
                                #print "s"+str(stage_i)+",t"+str(tree_i)+") right_val: "+ right_val.text
                            for feature in trees__.iter(tag='feature'):
                                #z = cascade()
                                self.stage[stage_i].tree[tree_i].feature = cascade()
                                for tilted in trees__.iter(tag='tilted'):
                                    self.stage[stage_i].tree[tree_i].feature.tilted = tilted.text
                                    #print "s"+str(stage_i)+",t"+str(tree_i)+") tilted: "+ tilted.text
                                self.stage[stage_i].tree[tree_i].feature.rect = []
                                for rects in trees__.iter(tag='rects'):
                                    rect_i=0
                                    for rect in rects:
                                        z = cascade()
                                        self.stage[stage_i].tree[tree_i].feature.rect.append(z)
                                        r = rect.text.split(" ")
                                        self.stage[stage_i].tree[tree_i].feature.rect[rect_i].x = Decimal(r[0])
                                        self.stage[stage_i].tree[tree_i].feature.rect[rect_i].y = Decimal(r[1])
                                        self.stage[stage_i].tree[tree_i].feature.rect[rect_i].w = Decimal(r[2])
                                        self.stage[stage_i].tree[tree_i].feature.rect[rect_i].h = Decimal(r[3])
                                        self.stage[stage_i].tree[tree_i].feature.rect[rect_i].weight = Decimal(r[4])
                                        #print "s"+str(stage_i)+",t"+str(tree_i)+",r"+ str(rect_i)+") rect: "+ rect.text
                                        rect_i=rect_i+1
                                    self.stage[stage_i].tree[tree_i].feature.rectSize = rect_i
                                    #print "rect size: "+ str(rect_i) 
                        tree_i = tree_i+1
                    #print "tree size: "+ str(tree_i) 
                    self.stage[stage_i].treeSize = tree_i
                    
                    #self.stage[stage_i].treeSize = tree_i
                    #self.stage.append(a)
                stage_i = stage_i+1
        #print "stage size: "+ str(stage_i)   
        self.stageSize  =  stage_i