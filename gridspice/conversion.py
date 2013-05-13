__author__ = "Jimmy Du and Kyle Anderson" 
__copyright__ = "Copyright 2013, The GridSpice Project" 
__license__ = "BSD" 
__version__ = "1.0" 
__maintainer__ = ["Kyle Anderson", "Jimmy Du"] 
__email__ = ["kyle.anderson@stanford.edu", "jimmydu@stanford.edu"] 
__status__ = "Development" 

def get_class_path(type): 
    return { 
        'billdump': 'element.powerflow.billdump.billdump',
        'currdump': 'element.powerflow.currdump.currdump',
        'emissions': 'element.powerflow.emissions.emissions',
        'fault_check': 'element.powerflow.fault_check.fault_check',
        'frequency_gen': 'element.powerflow.frequency_gen.frequency_gen',
        'line_configuration': 'element.powerflow.line_configuration.line_configuration',
        'line_spacing': 'element.powerflow.line_spacing.line_spacing',
        'overhead_line_conductor': 'element.powerflow.overhead_line_conductor.overhead_line_conductor',
        'power_metrics': 'element.powerflow.power_metrics.power_metrics',
        'powerflow_library': 'element.powerflow.powerflow_library.powerflow_library',
        'powerflow_object': 'element.powerflow.powerflow_object.powerflow_object',
        'node': 'element.powerflow.powerflow_object.node',
        'link': 'element.powerflow.powerflow_object.link',
        'capacitor': 'element.powerflow.powerflow_object.capacitor',
        'fuse': 'element.powerflow.powerflow_object.fuse',
        'meter': 'element.powerflow.powerflow_object.meter',
        'line': 'element.powerflow.powerflow_object.line',
        'overhead_line': 'element.powerflow.powerflow_object.overhead_line',
        'underground_line': 'element.powerflow.powerflow_object.underground_line',
        'relay': 'element.powerflow.powerflow_object.relay',
        'transformer': 'element.powerflow.powerflow_object.transformer',
        'load': 'element.powerflow.powerflow_object.load',
        'regulator': 'element.powerflow.powerflow_object.regulator',
        'triplex_node': 'element.powerflow.powerflow_object.triplex_node',
        'triplex_meter': 'element.powerflow.powerflow_object.triplex_meter',
        'triplex_line': 'element.powerflow.powerflow_object.triplex_line',
        'switch': 'element.powerflow.powerflow_object.switch',
        'substation': 'element.powerflow.powerflow_object.substation',
        'pqload': 'element.powerflow.powerflow_object.pqload',
        'series_reactor': 'element.powerflow.powerflow_object.series_reactor',
        'motor': 'element.powerflow.powerflow_object.motor',
        'recloser': 'element.powerflow.powerflow_object.recloser',
        'sectionalizer': 'element.powerflow.powerflow_object.sectionalizer',
        'regulator_configuration': 'element.powerflow.regulator_configuration.regulator_configuration',
        'restoration': 'element.powerflow.restoration.restoration',
        'transformer_configuration': 'element.powerflow.transformer_configuration.transformer_configuration',
        'triplex_line_conductor': 'element.powerflow.triplex_line_conductor.triplex_line_conductor',
        'triplex_line_configuration': 'element.powerflow.triplex_line_configuration.triplex_line_configuration',
        'underground_line_conductor': 'element.powerflow.underground_line_conductor.underground_line_conductor',
        'volt_var_control': 'element.powerflow.volt_var_control.volt_var_control',
        'voltdump': 'element.powerflow.voltdump.voltdump',
        'areas': 'element.wholesale.areas.areas',
        'baseMVA': 'element.wholesale.baseMVA.baseMVA',
        'branch': 'element.wholesale.branch.branch',
        'bus': 'element.wholesale.bus.bus',
        'gen': 'element.wholesale.gen.gen',
        'gen_cost': 'element.wholesale.gen_cost.gen_cost',
    }.get(type, None) 
