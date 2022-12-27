import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_Utility as AllplanUtil
import GeometryValidate as GeometryValidate
from HandleDirection import HandleDirection
from HandleProperties import HandleProperties


def check_version(build_section, version):
    del build_section
    del version
    return True


def create_element(build_section, doc):
    element = Beam_of_bridge(doc)
    return element.create(build_section)


class Beam_of_bridge:
    def __init__(self, doc):
        self.model_ele_list = []
        self.handle_list = []
        self.document = doc

    def create(self, build_section):
        self.connect_all_parts(build_section)
        self.create_lower_part_beam_of_bridge(build_section)
        return (self.model_ele_list, self.handle_list)

    def connect_all_parts(self, build_section):
        com_prop = AllplanBaseElements.CommonProperties()
        com_prop.GetGlobalProperties()
        com_prop.Pen = 1
        com_prop.Color = 3
        com_prop.Stroke = 1
        polyhedron_bottom = self.create_lower_part_beam_of_bridge(build_section)
        polyhedron_center = self.create_central_part_beam_of_bridge(build_section)
        polyhedron_top = self.create_top_part_beam_of_bridge(build_section)
        err, polyhedron = AllplanGeo.MakeUnion(polyhedron_bottom, polyhedron_center)
        if err:
            return
        err, polyhedron = AllplanGeo.MakeUnion(polyhedron, polyhedron_top)
        if err:
            return 
        self.model_ele_list.append(
            AllplanBasisElements.ModelElement3D(com_prop, polyhedron))

    # must be updated
    def create_lower_part_beam_of_bridge(self, build_section):
        polyhedron = self.lower_part_addiction_1(build_section)
        err, polyhedron = AllplanGeo.MakeUnion(polyhedron, self.lower_part_addiction_2(build_section))
        err, polyhedron = AllplanGeo.MakeUnion(polyhedron, self.lower_part_addiction_3(build_section))
        err, polyhedron = AllplanGeo.MakeUnion(polyhedron, self.lower_part_addiction_4(build_section))
        err, polyhedron = AllplanGeo.MakeUnion(polyhedron, self.lower_part_addiction_2_2(build_section))
        err, polyhedron = AllplanGeo.MakeUnion(polyhedron, self.lower_part_addiction_3_2(build_section))
        err, polyhedron = AllplanGeo.MakeUnion(polyhedron, self.lower_part_addiction_4_2(build_section))
        err, polyhedron = AllplanGeo.MakeUnion(polyhedron, self.lower_part_addiction_2_3(build_section))
        err, polyhedron = AllplanGeo.MakeUnion(polyhedron, self.lower_part_addiction_3_3(build_section))
        err, polyhedron = AllplanGeo.MakeUnion(polyhedron, self.lower_part_addiction_2_4(build_section))
        err, polyhedron = AllplanGeo.MakeUnion(polyhedron, self.lower_part_addiction_3_4(build_section))
        err, polyhedron = AllplanGeo.MakeUnion(polyhedron, self.last_lower_part(build_section))
        return polyhedron

    def create_central_part_beam_of_bridge(self, build_section):
        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(0, build_section.LengthFirst.value, build_section.HeightSecond.value)
        base_pol += AllplanGeo.Point3D(0, build_section.WidthFirst.value - build_section.LengthFirst.value, build_section.HeightSecond.value)
        base_pol += AllplanGeo.Point3D(build_section.LengthSecondd.value, build_section.WidthFirst.value - build_section.LengthFirst.value, build_section.HeightSecond.value)
        base_pol += AllplanGeo.Point3D(build_section.LengthSecondd.value + build_section.Transition_lenght.value, 
                                        build_section.WidthFirst.value - build_section.LengthFirst.value - (build_section.WidthFirst.value - build_section.LengthFirst.value * 2 - build_section.WidthSecondd.value) / 2, 
                                        build_section.HeightSecond.value)
        base_pol += AllplanGeo.Point3D(build_section.Length.value - (build_section.LengthSecondd.value + build_section.Transition_lenght.value), 
                                        build_section.WidthFirst.value - build_section.LengthFirst.value - (build_section.WidthFirst.value - build_section.LengthFirst.value * 2 - build_section.WidthSecondd.value) / 2, 
                                        build_section.HeightSecond.value)
        base_pol += AllplanGeo.Point3D(build_section.Length.value - build_section.LengthSecondd.value,
                                         build_section.WidthFirst.value - build_section.LengthFirst.value, 
                                         build_section.HeightSecond.value)
        base_pol += AllplanGeo.Point3D(build_section.Length.value, build_section.WidthFirst.value - build_section.LengthFirst.value, build_section.HeightSecond.value)
        base_pol += AllplanGeo.Point3D(build_section.Length.value, build_section.LengthFirst.value, build_section.HeightSecond.value)
        base_pol += AllplanGeo.Point3D(build_section.Length.value - build_section.LengthSecondd.value, build_section.LengthFirst.value, build_section.HeightSecond.value)
        base_pol += AllplanGeo.Point3D(build_section.Length.value - build_section.LengthSecondd.value - build_section.Transition_lenght.value,
                                        build_section.LengthFirst.value + (build_section.WidthFirst.value - build_section.LengthFirst.value * 2 - build_section.WidthSecondd.value) / 2, 
                                        build_section.HeightSecond.value)
        base_pol += AllplanGeo.Point3D(build_section.LengthSecondd.value + build_section.Transition_lenght.value,
                                        build_section.LengthFirst.value + (build_section.WidthFirst.value - build_section.LengthFirst.value * 2 - build_section.WidthSecondd.value) / 2, 
                                        build_section.HeightSecond.value)
        base_pol += AllplanGeo.Point3D(build_section.LengthSecondd.value,
                                        build_section.LengthFirst.value, 
                                        build_section.HeightSecond.value)
        base_pol += AllplanGeo.Point3D(0, build_section.LengthFirst.value, build_section.HeightSecond.value)


        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(0, build_section.LengthFirst.value, build_section.HeightSecond.value)
        path += AllplanGeo.Point3D(0, build_section.LengthFirst.value, build_section.HeightSecond.value + build_section.HeightThird.value)

        err, polyhedron = AllplanGeo.CreatePolyhedron(base_pol, path)

        if err:
            return []

        return polyhedron

    def create_top_part_beam_of_bridge(self, build_section):
        polyhedron = self.top_part_addiction_1(build_section)
        err, polyhedron = AllplanGeo.MakeUnion(polyhedron, self.top_part_addiction_3(build_section))
        err, polyhedron = AllplanGeo.MakeUnion(polyhedron, self.top_part_addiction_2(build_section))
        err, polyhedron = AllplanGeo.MakeUnion(polyhedron, self.top_part_addiction_3(build_section, plus=(build_section.Length.value - build_section.LengthSecondd.value)))
        err, polyhedron = AllplanGeo.MakeUnion(polyhedron, self.top_part_addiction_4(build_section))
        err, polyhedron = AllplanGeo.MakeUnion(polyhedron, self.top_part_addiction_2_2(build_section))
        err, polyhedron = AllplanGeo.MakeUnion(polyhedron, self.top_part_addiction_4(build_section, build_section.WidthFirst.value - build_section.LengthFirst.value * 2, build_section.WidthThird.value, 10))
        err, polyhedron = AllplanGeo.MakeUnion(polyhedron, self.top_part_addiction_2_3(build_section))
        err, polyhedron = AllplanGeo.MakeUnion(polyhedron, self.top_part_addiction_4_2(build_section))
        err, polyhedron = AllplanGeo.MakeUnion(polyhedron, self.top_part_addiction_4_2(build_section, build_section.WidthFirst.value - build_section.LengthFirst.value * 2, build_section.WidthThird.value, 10))
        err, polyhedron = AllplanGeo.MakeUnion(polyhedron, self.top_part_addiction_3_3(build_section))
        err, polyhedron = AllplanGeo.MakeUnion(polyhedron, self.last_top_part(build_section))
        return polyhedron

    def top_part_addiction_1(self, build_section):
        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(build_section.LengthSecondd.value, 
                                        build_section.WidthFirst.value - build_section.LengthFirst.value - (build_section.WidthFirst.value - build_section.LengthFirst.value * 2 - build_section.WidthSecondd.value) / 2,
                                        build_section.HeightSecond.value + build_section.HeightThird.value)
        base_pol += AllplanGeo.Point3D(build_section.LengthSecondd.value, 
                                        build_section.WidthThird.value - (build_section.WidthThird.value - build_section.WidthFirst.value) / 2,
                                        build_section.HeightSecond.value + build_section.HeightThird.value + build_section.HeightFourth.value)
        base_pol += AllplanGeo.Point3D(build_section.LengthSecondd.value, 
                                        -(build_section.WidthThird.value - build_section.WidthFirst.value) / 2,
                                        build_section.HeightSecond.value + build_section.HeightThird.value + build_section.HeightFourth.value)
        base_pol += AllplanGeo.Point3D(build_section.LengthSecondd.value, 
                                        build_section.LengthFirst.value + (build_section.WidthFirst.value - build_section.LengthFirst.value * 2 - build_section.WidthSecondd.value) / 2,
                                        build_section.HeightSecond.value + build_section.HeightThird.value)
        base_pol += AllplanGeo.Point3D(build_section.LengthSecondd.value, 
                                        build_section.WidthFirst.value - build_section.LengthFirst.value - (build_section.WidthFirst.value - build_section.LengthFirst.value * 2 - build_section.WidthSecondd.value) / 2,
                                        build_section.HeightSecond.value + build_section.HeightThird.value)
        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(build_section.LengthSecondd.value, 
                                        build_section.WidthFirst.value - build_section.LengthFirst.value - (build_section.WidthFirst.value - build_section.LengthFirst.value * 2 - build_section.WidthSecondd.value) / 2,
                                        build_section.HeightSecond.value + build_section.HeightThird.value)
        path += AllplanGeo.Point3D(build_section.Length.value - build_section.LengthSecondd.value, 
                                        build_section.WidthFirst.value - build_section.LengthFirst.value - (build_section.WidthFirst.value - build_section.LengthFirst.value * 2 - build_section.WidthSecondd.value) / 2,
                                        build_section.HeightSecond.value + build_section.HeightThird.value)
        
        err, polyhedron = AllplanGeo.CreatePolyhedron(base_pol, path)

        if err:
            return []

        return polyhedron

    def top_part_addiction_2(self, build_section):
        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(build_section.Length.value - build_section.LengthSecondd.value, build_section.WidthFirst.value - build_section.LengthFirst.value, build_section.HeightSecond.value + build_section.HeightThird.value)
        base_pol += AllplanGeo.Point3D(build_section.Length.value - build_section.LengthSecondd.value - build_section.Transition_lenght.value, build_section.WidthFirst.value - build_section.LengthFirst.value - (build_section.WidthFirst.value - build_section.LengthFirst.value * 2 - build_section.WidthSecondd.value) / 2 , build_section.HeightSecond.value + build_section.HeightThird.value)
        base_pol += AllplanGeo.Point3D(build_section.Length.value - build_section.LengthSecondd.value - build_section.Transition_lenght.value - (build_section.WidthFirst.value - build_section.LengthFirst.value * 2 - build_section.WidthSecondd.value) / 2 , build_section.WidthFirst.value - (build_section.WidthFirst.value - build_section.LengthFirst.value * 2 - build_section.WidthSecondd.value) / 2 + (build_section.WidthThird.value - build_section.WidthFirst.value) / 2, build_section.HeightSecond.value + build_section.HeightThird.value + build_section.HeightFourth.value)
        base_pol += AllplanGeo.Point3D(build_section.Length.value - build_section.LengthSecondd.value - (build_section.WidthFirst.value - build_section.LengthFirst.value * 2 - build_section.WidthSecondd.value) / 2, build_section.WidthFirst.value + (build_section.WidthThird.value - build_section.WidthFirst.value) / 2, build_section.HeightSecond.value + build_section.HeightThird.value + build_section.HeightFourth.value)
        base_pol += AllplanGeo.Point3D(build_section.Length.value - build_section.LengthSecondd.value, build_section.WidthFirst.value - build_section.LengthFirst.value, build_section.HeightSecond.value + build_section.HeightThird.value)


        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(build_section.Length.value - build_section.LengthSecondd.value, build_section.WidthFirst.value - build_section.LengthFirst.value, build_section.HeightSecond.value + build_section.HeightThird.value)
        path += AllplanGeo.Point3D(build_section.Length.value - build_section.LengthSecondd.value + 10, build_section.WidthFirst.value - build_section.LengthFirst.value - 10, build_section.HeightSecond.value + build_section.HeightThird.value + 10)

        err, polyhedron = AllplanGeo.CreatePolyhedron(base_pol, path)

        
        if err:
            return []

        return polyhedron

    def top_part_addiction_3(self, build_section, plus=0):
        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(plus, build_section.LengthFirst.value, build_section.HeightSecond.value + build_section.HeightThird.value)
        base_pol += AllplanGeo.Point3D(plus, build_section.WidthFirst.value - build_section.LengthFirst.value, build_section.HeightSecond.value + build_section.HeightThird.value)
        base_pol += AllplanGeo.Point3D(plus, build_section.WidthFirst.value + (build_section.WidthThird.value - build_section.WidthFirst.value) / 2, build_section.HeightSecond.value + build_section.HeightThird.value + build_section.HeightFourth.value)
        base_pol += AllplanGeo.Point3D(plus, -(build_section.WidthThird.value - build_section.WidthFirst.value) / 2, build_section.HeightSecond.value + build_section.HeightThird.value + build_section.HeightFourth.value)
        base_pol += AllplanGeo.Point3D(plus, build_section.LengthFirst.value, build_section.HeightSecond.value + build_section.HeightThird.value)

        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(plus, build_section.LengthFirst.value, build_section.HeightSecond.value + build_section.HeightThird.value)
        path += AllplanGeo.Point3D(plus + build_section.LengthSecondd.value, build_section.LengthFirst.value, build_section.HeightSecond.value + build_section.HeightThird.value)

        err, polyhedron = AllplanGeo.CreatePolyhedron(base_pol, path)

        
        if err:
            return []

        return polyhedron

    def top_part_addiction_4(self, build_section, minus_1 = 0, minus_2 = 0, digit = -10):
        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(build_section.Length.value - build_section.LengthSecondd.value, build_section.WidthFirst.value - build_section.LengthFirst.value - minus_1, build_section.HeightSecond.value + build_section.HeightThird.value)
        base_pol += AllplanGeo.Point3D(build_section.Length.value - build_section.LengthSecondd.value, build_section.WidthThird.value - (build_section.WidthThird.value - build_section.WidthFirst.value) / 2 - minus_2, build_section.HeightSecond.value + build_section.HeightThird.value + build_section.HeightFourth.value)
        base_pol += AllplanGeo.Point3D(build_section.Length.value - build_section.LengthSecondd.value - (build_section.WidthFirst.value - build_section.LengthFirst.value * 2 - build_section.WidthSecondd.value) / 2, build_section.WidthFirst.value + (build_section.WidthThird.value - build_section.WidthFirst.value) / 2 - minus_2, build_section.HeightSecond.value + build_section.HeightThird.value + build_section.HeightFourth.value)
        base_pol += AllplanGeo.Point3D(build_section.Length.value - build_section.LengthSecondd.value, build_section.WidthFirst.value - build_section.LengthFirst.value - minus_1, build_section.HeightSecond.value + build_section.HeightThird.value)


        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(build_section.Length.value - build_section.LengthSecondd.value, build_section.WidthFirst.value - build_section.LengthFirst.value - minus_1, build_section.HeightSecond.value + build_section.HeightThird.value)
        path += AllplanGeo.Point3D(build_section.Length.value - build_section.LengthSecondd.value, build_section.WidthFirst.value - build_section.LengthFirst.value + digit - minus_1, build_section.HeightSecond.value + build_section.HeightThird.value)
        print(base_pol)
        print(path)
        err, polyhedron = AllplanGeo.CreatePolyhedron(base_pol, path)

        
        if err:
            return []

        return polyhedron

    def top_part_addiction_2_2(self, build_section):
        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(build_section.Length.value - build_section.LengthSecondd.value, build_section.LengthFirst.value, build_section.HeightSecond.value + build_section.HeightThird.value)
        base_pol += AllplanGeo.Point3D(build_section.Length.value - build_section.LengthSecondd.value - build_section.Transition_lenght.value, build_section.LengthFirst.value + (build_section.WidthFirst.value - build_section.LengthFirst.value * 2 - build_section.WidthSecondd.value) / 2, build_section.HeightSecond.value + build_section.HeightThird.value)
        base_pol += AllplanGeo.Point3D(build_section.Length.value - build_section.LengthSecondd.value - build_section.Transition_lenght.value - (build_section.WidthFirst.value - build_section.LengthFirst.value * 2 - build_section.WidthSecondd.value) / 2, (build_section.WidthFirst.value - build_section.LengthFirst.value * 2 - build_section.WidthSecondd.value) / 2 - (build_section.WidthThird.value - build_section.WidthFirst.value) / 2, build_section.HeightSecond.value + build_section.HeightThird.value + build_section.HeightFourth.value)
        base_pol += AllplanGeo.Point3D(build_section.Length.value - build_section.LengthSecondd.value - (build_section.WidthFirst.value - build_section.LengthFirst.value * 2 - build_section.WidthSecondd.value) / 2, -(build_section.WidthThird.value - build_section.WidthFirst.value) / 2, build_section.HeightSecond.value + build_section.HeightThird.value + build_section.HeightFourth.value)
        base_pol += AllplanGeo.Point3D(build_section.Length.value - build_section.LengthSecondd.value, build_section.LengthFirst.value, build_section.HeightSecond.value + build_section.HeightThird.value)


        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(build_section.Length.value - build_section.LengthSecondd.value, build_section.LengthFirst.value, build_section.HeightSecond.value + build_section.HeightThird.value)
        path += AllplanGeo.Point3D(build_section.Length.value - build_section.LengthSecondd.value + 10, build_section.LengthFirst.value + 10, build_section.HeightSecond.value + build_section.HeightThird.value + 10)

        err, polyhedron = AllplanGeo.CreatePolyhedron(base_pol, path)

        
        if err:
            return []

        return polyhedron

    def top_part_addiction_2_3(self, build_section):
        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(build_section.LengthSecondd.value, build_section.WidthFirst.value - build_section.LengthFirst.value, build_section.HeightSecond.value + build_section.HeightThird.value)
        base_pol += AllplanGeo.Point3D(build_section.LengthSecondd.value + build_section.Transition_lenght.value, build_section.WidthFirst.value - build_section.LengthFirst.value - (build_section.WidthFirst.value - build_section.LengthFirst.value * 2 - build_section.WidthSecondd.value) / 2, build_section.HeightSecond.value + build_section.HeightThird.value)
        base_pol += AllplanGeo.Point3D(build_section.LengthSecondd.value + build_section.Transition_lenght.value + (build_section.WidthFirst.value - build_section.LengthFirst.value * 2 - build_section.WidthSecondd.value) / 2, build_section.WidthFirst.value - (build_section.WidthFirst.value - build_section.LengthFirst.value * 2 - build_section.WidthSecondd.value) / 2 + (build_section.WidthThird.value - build_section.WidthFirst.value) / 2, build_section.HeightSecond.value + build_section.HeightThird.value + build_section.HeightFourth.value)
        base_pol += AllplanGeo.Point3D(build_section.LengthSecondd.value + (build_section.WidthFirst.value - build_section.LengthFirst.value * 2 - build_section.WidthSecondd.value) / 2, build_section.WidthFirst.value + (build_section.WidthThird.value - build_section.WidthFirst.value) / 2, build_section.HeightSecond.value + build_section.HeightThird.value + build_section.HeightFourth.value)
        base_pol += AllplanGeo.Point3D(build_section.LengthSecondd.value, build_section.WidthFirst.value - build_section.LengthFirst.value, build_section.HeightSecond.value + build_section.HeightThird.value)


        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(build_section.LengthSecondd.value, build_section.WidthFirst.value - build_section.LengthFirst.value, build_section.HeightSecond.value + build_section.HeightThird.value)
        path += AllplanGeo.Point3D(build_section.LengthSecondd.value - 10, build_section.WidthFirst.value - build_section.LengthFirst.value - 10, build_section.HeightSecond.value + build_section.HeightThird.value - 10)

        err, polyhedron = AllplanGeo.CreatePolyhedron(base_pol, path)

        
        if err:
            return []

        return polyhedron

    def top_part_addiction_4_2(self, build_section, minus_1 = 0, minus_2 = 0, digit = -10):
        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(build_section.LengthSecondd.value, build_section.WidthFirst.value - build_section.LengthFirst.value - minus_1, build_section.HeightSecond.value + build_section.HeightThird.value)
        base_pol += AllplanGeo.Point3D(build_section.LengthSecondd.value, build_section.WidthFirst.value + (build_section.WidthThird.value - build_section.WidthFirst.value) / 2 - minus_2, build_section.HeightSecond.value + build_section.HeightThird.value + build_section.HeightFourth.value)
        base_pol += AllplanGeo.Point3D(build_section.LengthSecondd.value + (build_section.WidthFirst.value - build_section.LengthFirst.value * 2 - build_section.WidthSecondd.value) / 2, build_section.WidthFirst.value + (build_section.WidthThird.value - build_section.WidthFirst.value) / 2 - minus_2, build_section.HeightSecond.value + build_section.HeightThird.value + build_section.HeightFourth.value)
        base_pol += AllplanGeo.Point3D(build_section.LengthSecondd.value, build_section.WidthFirst.value - build_section.LengthFirst.value - minus_1, build_section.HeightSecond.value + build_section.HeightThird.value)
        
        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(build_section.LengthSecondd.value, build_section.WidthFirst.value - build_section.LengthFirst.value - minus_1, build_section.HeightSecond.value + build_section.HeightThird.value)
        path += AllplanGeo.Point3D(build_section.LengthSecondd.value, build_section.WidthFirst.value - build_section.LengthFirst.value - minus_1 + digit, build_section.HeightSecond.value + build_section.HeightThird.value)

        err, polyhedron = AllplanGeo.CreatePolyhedron(base_pol, path)

        if err:
            return []

        return polyhedron

    def top_part_addiction_3_3(self, build_section):
        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(build_section.LengthSecondd.value, build_section.LengthFirst.value, build_section.HeightSecond.value + build_section.HeightThird.value)
        base_pol += AllplanGeo.Point3D(build_section.LengthSecondd.value + build_section.Transition_lenght.value, build_section.LengthFirst.value + (build_section.WidthFirst.value - build_section.LengthFirst.value * 2 - build_section.WidthSecondd.value) / 2, build_section.HeightSecond.value + build_section.HeightThird.value)
        base_pol += AllplanGeo.Point3D(build_section.LengthSecondd.value + build_section.Transition_lenght.value + (build_section.WidthFirst.value - build_section.LengthFirst.value * 2 - build_section.WidthSecondd.value) / 2, (build_section.WidthFirst.value - build_section.LengthFirst.value * 2 - build_section.WidthSecondd.value) / 2 - (build_section.WidthThird.value - build_section.WidthFirst.value) / 2, build_section.HeightSecond.value + build_section.HeightThird.value + build_section.HeightFourth.value)
        base_pol += AllplanGeo.Point3D(build_section.LengthSecondd.value + (build_section.WidthFirst.value - build_section.LengthFirst.value * 2 - build_section.WidthSecondd.value) / 2, -(build_section.WidthThird.value - build_section.WidthFirst.value) / 2, build_section.HeightSecond.value + build_section.HeightThird.value + build_section.HeightFourth.value)
        base_pol += AllplanGeo.Point3D(build_section.LengthSecondd.value, build_section.LengthFirst.value, build_section.HeightSecond.value + build_section.HeightThird.value)


        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(build_section.LengthSecondd.value, build_section.LengthFirst.value, build_section.HeightSecond.value + build_section.HeightThird.value)
        path += AllplanGeo.Point3D(build_section.LengthSecondd.value - 10, build_section.LengthFirst.value + 10, build_section.HeightSecond.value + build_section.HeightThird.value - 10)

        err, polyhedron = AllplanGeo.CreatePolyhedron(base_pol, path)

        
        if err:
            return []

        return polyhedron

    def last_top_part(self, build_section):
        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(0, -(build_section.WidthThird.value - build_section.WidthFirst.value) / 2, build_section.HeightSecond.value + build_section.HeightThird.value + build_section.HeightFourth.value)
        base_pol += AllplanGeo.Point3D(0, build_section.WidthThird.value - (build_section.WidthThird.value - build_section.WidthFirst.value) / 2, build_section.HeightSecond.value + build_section.HeightThird.value + build_section.HeightFourth.value)
        base_pol += AllplanGeo.Point3D(0, build_section.WidthThird.value - (build_section.WidthThird.value - build_section.WidthFirst.value) / 2, build_section.HeightSecond.value + build_section.HeightThird.value + build_section.HeightThirdd.value)
        base_pol += AllplanGeo.Point3D(0, build_section.WidthThird.value - (build_section.WidthThird.value - build_section.WidthFirst.value) / 2 - build_section.Identation.value, build_section.HeightSecond.value + build_section.HeightThird.value + build_section.HeightThirdd.value)
        base_pol += AllplanGeo.Point3D(0, build_section.WidthThird.value - (build_section.WidthThird.value - build_section.WidthFirst.value) / 2 - build_section.Identation.value, build_section.HeightSecond.value + build_section.HeightThird.value + build_section.HeightThirdd.value + build_section.Plate_height.value)
        base_pol += AllplanGeo.Point3D(0, - (build_section.WidthThird.value - build_section.WidthFirst.value) / 2 + build_section.Identation.value, build_section.HeightSecond.value + build_section.HeightThird.value + build_section.HeightThirdd.value + build_section.Plate_height.value)
        base_pol += AllplanGeo.Point3D(0, - (build_section.WidthThird.value - build_section.WidthFirst.value) / 2 + build_section.Identation.value, build_section.HeightSecond.value + build_section.HeightThird.value + build_section.HeightThirdd.value)
        base_pol += AllplanGeo.Point3D(0, - (build_section.WidthThird.value - build_section.WidthFirst.value) / 2, build_section.HeightSecond.value + build_section.HeightThird.value + build_section.HeightThirdd.value)
        base_pol += AllplanGeo.Point3D(0, -(build_section.WidthThird.value - build_section.WidthFirst.value) / 2, build_section.HeightSecond.value + build_section.HeightThird.value + build_section.HeightFourth.value)

        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(0, -(build_section.WidthThird.value - build_section.WidthFirst.value) / 2, build_section.HeightSecond.value + build_section.HeightThird.value + build_section.HeightFourth.value)
        path += AllplanGeo.Point3D(build_section.Length.value, -(build_section.WidthThird.value - build_section.WidthFirst.value) / 2, build_section.HeightSecond.value + build_section.HeightThird.value + build_section.HeightFourth.value)
        err, polyhedron = AllplanGeo.CreatePolyhedron(base_pol, path)

        
        if err:
            return []

        return polyhedron

    def lower_part_addiction_1(self, build_section):
        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(build_section.LengthSecondd.value, build_section.WidthFirst.value, build_section.HeightSecond.value - build_section.HeightFirst.value)
        base_pol += AllplanGeo.Point3D(build_section.LengthSecondd.value, 
                                    build_section.WidthFirst.value - build_section.LengthFirst.value - (build_section.WidthFirst.value - build_section.LengthFirst.value * 2 - build_section.WidthSecondd.value) / 2,
                                    build_section.HeightSecond.value)
        base_pol += AllplanGeo.Point3D(build_section.LengthSecondd.value, 
                                    build_section.WidthFirst.value - build_section.LengthFirst.value - (build_section.WidthFirst.value - build_section.LengthFirst.value * 2 - build_section.WidthSecondd.value) / 2 - build_section.WidthSecondd.value,
                                    build_section.HeightSecond.value)
        base_pol += AllplanGeo.Point3D(build_section.LengthSecondd.value, 0, build_section.HeightSecond.value - build_section.HeightFirst.value)
        base_pol += AllplanGeo.Point3D(build_section.LengthSecondd.value, build_section.WidthFirst.value, build_section.HeightSecond.value - build_section.HeightFirst.value)

        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(build_section.LengthSecondd.value, build_section.WidthFirst.value, build_section.HeightSecond.value - build_section.HeightFirst.value)
        path += AllplanGeo.Point3D(build_section.Length.value - build_section.LengthSecondd.value, build_section.WidthFirst.value, build_section.HeightSecond.value - build_section.HeightFirst.value)
        err, polyhedron = AllplanGeo.CreatePolyhedron(base_pol, path)

        if err:
            return []

        return polyhedron
    
    def lower_part_addiction_2(self, build_section):
        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(build_section.LengthSecondd.value, build_section.WidthFirst.value - build_section.LengthFirst.value, build_section.HeightSecond.value)
        base_pol += AllplanGeo.Point3D(build_section.LengthSecondd.value + build_section.Transition_lenght.value, build_section.WidthFirst.value - build_section.LengthFirst.value - (build_section.WidthFirst.value - build_section.LengthFirst.value * 2 - build_section.WidthSecondd.value) / 2, build_section.HeightSecond.value)
        base_pol += AllplanGeo.Point3D(build_section.LengthSecondd.value + build_section.Transition_lenght.value + (build_section.WidthFirst.value - build_section.LengthFirst.value * 2 - build_section.WidthSecondd.value) / 2, build_section.WidthFirst.value - (build_section.WidthFirst.value - build_section.LengthFirst.value * 2 - build_section.WidthSecondd.value) / 2, build_section.HeightSecond.value - build_section.HeightFirst.value)
        base_pol += AllplanGeo.Point3D(build_section.LengthSecondd.value + (build_section.WidthFirst.value - build_section.LengthFirst.value * 2 - build_section.WidthSecondd.value) / 2, build_section.WidthFirst.value, build_section.HeightSecond.value - build_section.HeightFirst.value)
        base_pol += AllplanGeo.Point3D(build_section.LengthSecondd.value, build_section.WidthFirst.value - build_section.LengthFirst.value, build_section.HeightSecond.value)


        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(build_section.LengthSecondd.value, build_section.WidthFirst.value - build_section.LengthFirst.value, build_section.HeightSecond.value)
        path += AllplanGeo.Point3D(build_section.LengthSecondd.value - 10 , build_section.WidthFirst.value - build_section.LengthFirst.value - 10, build_section.HeightSecond.value - 10)

        err, polyhedron = AllplanGeo.CreatePolyhedron(base_pol, path)

        
        if err:
            return []

        return polyhedron

    def lower_part_addiction_3(self, build_section):
        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(0, build_section.WidthFirst.value, build_section.HeightSecond.value - build_section.HeightFirst.value)
        base_pol += AllplanGeo.Point3D(0, build_section.WidthFirst.value - build_section.LengthFirst.value, build_section.HeightSecond.value)
        base_pol += AllplanGeo.Point3D(0, build_section.LengthFirst.value, build_section.HeightSecond.value)
        base_pol += AllplanGeo.Point3D(0, 0, build_section.HeightSecond.value - build_section.HeightFirst.value)
        base_pol += AllplanGeo.Point3D(0, build_section.WidthFirst.value, build_section.HeightSecond.value - build_section.HeightFirst.value)

        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(0, build_section.WidthFirst.value, build_section.HeightSecond.value - build_section.HeightFirst.value)
        path += AllplanGeo.Point3D(build_section.LengthSecondd.value, build_section.WidthFirst.value, build_section.HeightSecond.value - build_section.HeightFirst.value)

        err, polyhedron = AllplanGeo.CreatePolyhedron(base_pol, path)

        
        if err:
            return []

        return polyhedron

    def lower_part_addiction_4(self, build_section):
        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(build_section.LengthSecondd.value, build_section.WidthFirst.value - build_section.LengthFirst.value, build_section.HeightSecond.value)
        base_pol += AllplanGeo.Point3D(build_section.LengthSecondd.value, build_section.WidthFirst.value, build_section.HeightSecond.value - build_section.HeightFirst.value)
        base_pol += AllplanGeo.Point3D(build_section.LengthSecondd.value + (build_section.WidthFirst.value - build_section.LengthFirst.value * 2 - build_section.WidthSecondd.value) / 2, build_section.WidthFirst.value, build_section.HeightSecond.value - build_section.HeightFirst.value)
        base_pol += AllplanGeo.Point3D(build_section.LengthSecondd.value, build_section.WidthFirst.value - build_section.LengthFirst.value, build_section.HeightSecond.value)
        
        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(build_section.LengthSecondd.value, build_section.WidthFirst.value - build_section.LengthFirst.value, build_section.HeightSecond.value)
        path += AllplanGeo.Point3D(build_section.LengthSecondd.value, build_section.WidthFirst.value - build_section.LengthFirst.value - 10, build_section.HeightSecond.value)

        err, polyhedron = AllplanGeo.CreatePolyhedron(base_pol, path)

        if err:
            return []

        return polyhedron

    def lower_part_addiction_2_2(self, build_section):
        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(build_section.LengthSecondd.value, build_section.LengthFirst.value, build_section.HeightSecond.value)
        base_pol += AllplanGeo.Point3D(build_section.LengthSecondd.value + build_section.Transition_lenght.value, build_section.LengthFirst.value + (build_section.WidthFirst.value - build_section.LengthFirst.value * 2 - build_section.WidthSecondd.value) / 2, build_section.HeightSecond.value)
        base_pol += AllplanGeo.Point3D(build_section.LengthSecondd.value + build_section.Transition_lenght.value + (build_section.WidthFirst.value - build_section.LengthFirst.value * 2 - build_section.WidthSecondd.value) / 2, (build_section.WidthFirst.value - build_section.LengthFirst.value * 2 - build_section.WidthSecondd.value) / 2, build_section.HeightSecond.value - build_section.HeightFirst.value)
        base_pol += AllplanGeo.Point3D(build_section.LengthSecondd.value + (build_section.WidthFirst.value - build_section.LengthFirst.value * 2 - build_section.WidthSecondd.value) / 2, 0, build_section.HeightSecond.value - build_section.HeightFirst.value)
        base_pol += AllplanGeo.Point3D(build_section.LengthSecondd.value,build_section.LengthFirst.value, build_section.HeightSecond.value)


        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(build_section.LengthSecondd.value,build_section.LengthFirst.value, build_section.HeightSecond.value)
        path += AllplanGeo.Point3D(build_section.LengthSecondd.value - 10 ,build_section.LengthFirst.value + 10, build_section.HeightSecond.value - 10)

        err, polyhedron = AllplanGeo.CreatePolyhedron(base_pol, path)

        
        if err:
            return []

        return polyhedron

    def lower_part_addiction_3_2(self, build_section):
        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(build_section.Length.value - build_section.LengthSecondd.value, build_section.WidthFirst.value, build_section.HeightSecond.value - build_section.HeightFirst.value)
        base_pol += AllplanGeo.Point3D(build_section.Length.value - build_section.LengthSecondd.value, build_section.WidthFirst.value - build_section.LengthFirst.value, build_section.HeightSecond.value)
        base_pol += AllplanGeo.Point3D(build_section.Length.value - build_section.LengthSecondd.value, build_section.LengthFirst.value, build_section.HeightSecond.value)
        base_pol += AllplanGeo.Point3D(build_section.Length.value - build_section.LengthSecondd.value, 0, build_section.HeightSecond.value - build_section.HeightFirst.value)
        base_pol += AllplanGeo.Point3D(build_section.Length.value - build_section.LengthSecondd.value, build_section.WidthFirst.value, build_section.HeightSecond.value - build_section.HeightFirst.value)

        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(build_section.Length.value - build_section.LengthSecondd.value, build_section.WidthFirst.value, build_section.HeightSecond.value - build_section.HeightFirst.value)
        path += AllplanGeo.Point3D(build_section.Length.value, build_section.WidthFirst.value, build_section.HeightSecond.value - build_section.HeightFirst.value)

        err, polyhedron = AllplanGeo.CreatePolyhedron(base_pol, path)

        
        if err:
            return []

        return polyhedron

    def lower_part_addiction_4_2(self, build_section):
        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(build_section.LengthSecondd.value, build_section.LengthFirst.value, build_section.HeightSecond.value)
        base_pol += AllplanGeo.Point3D(build_section.LengthSecondd.value, 0, build_section.HeightSecond.value - build_section.HeightFirst.value)
        base_pol += AllplanGeo.Point3D(build_section.LengthSecondd.value + (build_section.WidthFirst.value - build_section.LengthFirst.value * 2 - build_section.WidthSecondd.value) / 2, 0, build_section.HeightSecond.value - build_section.HeightFirst.value)
        base_pol += AllplanGeo.Point3D(build_section.LengthSecondd.value, build_section.LengthFirst.value, build_section.HeightSecond.value)
        
        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(build_section.LengthSecondd.value, build_section.LengthFirst.value, build_section.HeightSecond.value)
        path += AllplanGeo.Point3D(build_section.LengthSecondd.value, build_section.LengthFirst.value + 10, build_section.HeightSecond.value)

        err, polyhedron = AllplanGeo.CreatePolyhedron(base_pol, path)

        if err:
            return []

        return polyhedron

    def lower_part_addiction_2_3(self, build_section):
        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(build_section.Length.value - build_section.LengthSecondd.value, build_section.WidthFirst.value - build_section.LengthFirst.value, build_section.HeightSecond.value)
        base_pol += AllplanGeo.Point3D(build_section.Length.value - build_section.LengthSecondd.value - build_section.Transition_lenght.value, build_section.WidthFirst.value - build_section.LengthFirst.value - (build_section.WidthFirst.value - build_section.LengthFirst.value * 2 - build_section.WidthSecondd.value) / 2, build_section.HeightSecond.value)
        base_pol += AllplanGeo.Point3D(build_section.Length.value - build_section.LengthSecondd.value - build_section.Transition_lenght.value - (build_section.WidthFirst.value - build_section.LengthFirst.value * 2 - build_section.WidthSecondd.value) / 2, build_section.WidthFirst.value - (build_section.WidthFirst.value - build_section.LengthFirst.value * 2 - build_section.WidthSecondd.value) / 2, build_section.HeightSecond.value - build_section.HeightFirst.value)
        base_pol += AllplanGeo.Point3D(build_section.Length.value - build_section.LengthSecondd.value - (build_section.WidthFirst.value - build_section.LengthFirst.value * 2 - build_section.WidthSecondd.value) / 2, build_section.WidthFirst.value, build_section.HeightSecond.value - build_section.HeightFirst.value)
        base_pol += AllplanGeo.Point3D(build_section.Length.value - build_section.LengthSecondd.value, build_section.WidthFirst.value - build_section.LengthFirst.value, build_section.HeightSecond.value)


        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(build_section.Length.value - build_section.LengthSecondd.value, build_section.WidthFirst.value - build_section.LengthFirst.value, build_section.HeightSecond.value)
        path += AllplanGeo.Point3D(build_section.Length.value - build_section.LengthSecondd.value + 10, build_section.WidthFirst.value - build_section.LengthFirst.value - 10, build_section.HeightSecond.value + 10)

        err, polyhedron = AllplanGeo.CreatePolyhedron(base_pol, path)

        
        if err:
            return []

        return polyhedron

    def lower_part_addiction_3_3(self, build_section):
        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(build_section.Length.value - build_section.LengthSecondd.value, build_section.WidthFirst.value - build_section.LengthFirst.value, build_section.HeightSecond.value)
        base_pol += AllplanGeo.Point3D(build_section.Length.value - build_section.LengthSecondd.value, build_section.WidthFirst.value, build_section.HeightSecond.value - build_section.HeightFirst.value)
        base_pol += AllplanGeo.Point3D(build_section.Length.value - build_section.LengthSecondd.value - (build_section.WidthFirst.value - build_section.LengthFirst.value * 2 - build_section.WidthSecondd.value) / 2, build_section.WidthFirst.value, build_section.HeightSecond.value - build_section.HeightFirst.value)
        base_pol += AllplanGeo.Point3D(build_section.Length.value - build_section.LengthSecondd.value, build_section.WidthFirst.value - build_section.LengthFirst.value, build_section.HeightSecond.value)


        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(build_section.Length.value - build_section.LengthSecondd.value, build_section.WidthFirst.value - build_section.LengthFirst.value, build_section.HeightSecond.value)
        path += AllplanGeo.Point3D(build_section.Length.value - build_section.LengthSecondd.value, build_section.WidthFirst.value - build_section.LengthFirst.value - 10, build_section.HeightSecond.value)

        err, polyhedron = AllplanGeo.CreatePolyhedron(base_pol, path)

        
        if err:
            return []

        return polyhedron

    def lower_part_addiction_2_4(self, build_section):
        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(build_section.Length.value - build_section.LengthSecondd.value, build_section.LengthFirst.value, build_section.HeightSecond.value)
        base_pol += AllplanGeo.Point3D(build_section.Length.value - build_section.LengthSecondd.value - build_section.Transition_lenght.value, build_section.LengthFirst.value + (build_section.WidthFirst.value - build_section.LengthFirst.value * 2 - build_section.WidthSecondd.value) / 2, build_section.HeightSecond.value)
        base_pol += AllplanGeo.Point3D(build_section.Length.value - build_section.LengthSecondd.value - build_section.Transition_lenght.value - (build_section.WidthFirst.value - build_section.LengthFirst.value * 2 - build_section.WidthSecondd.value) / 2, (build_section.WidthFirst.value - build_section.LengthFirst.value * 2 - build_section.WidthSecondd.value) / 2, build_section.HeightSecond.value - build_section.HeightFirst.value)
        base_pol += AllplanGeo.Point3D(build_section.Length.value - build_section.LengthSecondd.value - (build_section.WidthFirst.value - build_section.LengthFirst.value * 2 - build_section.WidthSecondd.value) / 2, 0, build_section.HeightSecond.value - build_section.HeightFirst.value)
        base_pol += AllplanGeo.Point3D(build_section.Length.value - build_section.LengthSecondd.value, build_section.LengthFirst.value, build_section.HeightSecond.value)


        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(build_section.Length.value - build_section.LengthSecondd.value, build_section.LengthFirst.value, build_section.HeightSecond.value)
        path += AllplanGeo.Point3D(build_section.Length.value - build_section.LengthSecondd.value - 10, build_section.LengthFirst.value + 10, build_section.HeightSecond.value - 10)

        err, polyhedron = AllplanGeo.CreatePolyhedron(base_pol, path)

        
        if err:
            return []

        return polyhedron

    def lower_part_addiction_3_4(self, build_section):
        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(build_section.Length.value - build_section.LengthSecondd.value, build_section.LengthFirst.value, build_section.HeightSecond.value)
        base_pol += AllplanGeo.Point3D(build_section.Length.value - build_section.LengthSecondd.value, 0, build_section.HeightSecond.value - build_section.HeightFirst.value)
        base_pol += AllplanGeo.Point3D(build_section.Length.value - build_section.LengthSecondd.value - (build_section.WidthFirst.value - build_section.LengthFirst.value * 2 - build_section.WidthSecondd.value) / 2, 0, build_section.HeightSecond.value - build_section.HeightFirst.value)
        base_pol += AllplanGeo.Point3D(build_section.Length.value - build_section.LengthSecondd.value, build_section.LengthFirst.value, build_section.HeightSecond.value)


        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(build_section.Length.value - build_section.LengthSecondd.value, build_section.LengthFirst.value, build_section.HeightSecond.value)
        path += AllplanGeo.Point3D(build_section.Length.value - build_section.LengthSecondd.value, build_section.LengthFirst.value + 10, build_section.HeightSecond.value)

        err, polyhedron = AllplanGeo.CreatePolyhedron(base_pol, path)

        
        if err:
            return []

        return polyhedron

    def last_lower_part(self, build_section):
        base_pol = AllplanGeo.Polygon3D()
        base_pol += AllplanGeo.Point3D(0, 20, 0)
        base_pol += AllplanGeo.Point3D(0, build_section.WidthFirst.value - 20, 0)
        base_pol += AllplanGeo.Point3D(0, build_section.WidthFirst.value, 20)
        base_pol += AllplanGeo.Point3D(0, build_section.WidthFirst.value, build_section.HeightSecond.value - build_section.HeightFirst.value)
        base_pol += AllplanGeo.Point3D(0, 0, build_section.HeightSecond.value - build_section.HeightFirst.value)
        base_pol += AllplanGeo.Point3D(0, 0, 20)
        base_pol += AllplanGeo.Point3D(0, 20, 0)

        if not GeometryValidate.is_valid(base_pol):
            return

        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(0, 20, 0)
        path += AllplanGeo.Point3D(build_section.Length.value,20,0)

        err, polyhedron = AllplanGeo.CreatePolyhedron(base_pol, path)

        
        if err:
            return []

        return polyhedron
