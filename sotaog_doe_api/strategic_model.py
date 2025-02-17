import fastapi
from fastapi.responses import FileResponse
from pareto.strategic_water_management.strategic_produced_water_optimization import (
    WaterQuality,
    create_model,
    Objectives,
    solve_model,
    PipelineCost,
    PipelineCapacity,
    Hydraulics,
    RemovalEfficiencyMethod,
    InfrastructureTiming,
    DesalinationModel,
    SubsurfaceRisk,
)
from pareto.utilities.get_data import get_data
from pareto.utilities.results import (
    generate_report,
    PrintValues,
    OutputUnits,
    is_feasible,
    nostdout,
)
# from pareto.utilities.visualize import plot_network
from importlib import resources

router = fastapi.APIRouter(prefix='/pareto',  tags=['Pareto'])
@router.post("/strategic-model")
def strategicModel():
    with resources.path(
        "pareto.case_studies",
        "strategic_toy_case_study.xlsx",
    ) as fpath:
        [df_sets, df_parameters] = get_data(fpath, model_type="strategic")
    strategic_model = create_model(
        df_sets,
        df_parameters,
        default={
            "objective": Objectives.cost,
            "pipeline_cost": PipelineCost.distance_based,
            "pipeline_capacity": PipelineCapacity.input,
            "hydraulics": Hydraulics.false,
            "desalination_model": DesalinationModel.false,
            "node_capacity": True,
            "water_quality": WaterQuality.false,
            "removal_efficiency_method": RemovalEfficiencyMethod.concentration_based,
            "infrastructure_timing": InfrastructureTiming.true,
            "subsurface_risk": SubsurfaceRisk.false,
        },
    )
    options = {
        "deactivate_slacks": True,
        "scale_model": False,
        "scaling_factor": 1000,
        "running_time": 200,
        "gap": 0,
    }

    results = solve_model(model=strategic_model, options=options)

    with nostdout():
        feasibility_status = is_feasible(strategic_model)

    if not feasibility_status:
        print("\nModel results are not feasible and should not be trusted\n" + "-" * 60)
    else:
        print("\nModel results validated and found to pass feasibility tests\n" + "-" * 60)
    print("\nConverting to Output Units and Displaying Solution\n" + "-" * 60)
        
    [model, results_dict] = generate_report(
        strategic_model,
        results_obj=results,
        is_print=PrintValues.essential,
        output_units=OutputUnits.user_units,
        fname="strategic_optimization_results.xlsx",
    )
    pos = {
        "PP01": (20, 20),
        "PP02": (45, 20),
        "PP03": (50, 50),
        "PP04": (80, 40),
        "CP01": (65, 20),
        "F01": (75, 15),
        "F02": (75, 25),
        "K01": (30, 10),
        "K02": (40, 50),
        "S02": (60, 50),
        "S03": (10, 44),
        "S04": (10, 36),
        "R01": (20, 40),
        "R02": (70, 50),
        "O01": (1, 55),
        "O02": (1, 40),
        "O03": (1, 25),
        "N01": (30, 20),
        "N02": (30, 30),
        "N03": (30, 40),
        "N04": (40, 40),
        "N05": (45, 30),
        "N06": (50, 40),
        "N07": (60, 40),
        "N08": (60, 30),
        "N09": (70, 40),
    }
    # plot_network(
    #     strategic_model,
    #     show_piping=True,
    #     show_trucking=True,
    #     show_results=False,
    #     save_fig="network.png",
    #     pos=pos,
    # )
    return {"message": "Success"}
