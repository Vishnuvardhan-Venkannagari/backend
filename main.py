import fastapi
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
import sys
import pkgutil
import importlib
from pareto.operational_water_management.operational_produced_water_optimization_model import (
    WaterQuality,
    create_model,
    ProdTank,
    postprocess_water_quality_calculation,
)
# from pareto.strategic_water_management.strategic_produced_water_optimization import (
#     WaterQuality,
#     create_model,
#     Objectives,
#     solve_model,
#     PipelineCost,
#     PipelineCapacity,
#     Hydraulics,
#     RemovalEfficiencyMethod,
#     InfrastructureTiming,
#     DesalinationModel,
#     SubsurfaceRisk,
# )
from pareto.utilities.get_data import get_data
from pareto.utilities.results import (
    generate_report,
    PrintValues,
    OutputUnits,
    is_feasible,
    nostdout,
)
# from pareto.utilities.visualize import plot_network
from pareto.utilities.solvers import get_solver, set_timeout
from importlib import resources

import pandas as pd

# app = FastAPI()
app = fastapi.FastAPI(version='1.0.0',
                      description=f"RestAPI for SOTAOG-DOE Platform",
                      openapi_url="/openapi.json",
                      title="SOTAOG-DOE")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://localhost:3000"],  # Add other necessary origins
    allow_credentials=True,
    allow_methods=["*"],  # Ensure all methods (GET, POST, etc.) are allowed
    allow_headers=["*"],  # Ensure all headers (including 'authtoken') are allowed
)

package_dir = os.getcwd() + "/sotaog_doe_api"
sys.path.append(os.path.abspath(package_dir))
@app.on_event("startup")
def onStart():
    # print("Onstart", package_dir)
    for module_info in pkgutil.iter_modules([str(package_dir)]):
        module = importlib.import_module(f'{module_info.name}')#routers.
        print(module_info.name)
        # print(hasattr(module, 'router'))
        if hasattr(module, 'router'):
            print(f'Including router from module: {module_info.name}', module.router)
            app.include_router(module.router, prefix="/api")
    print("Registered Routes:")
    for route in app.routes:
        print(f"Path: {route.path}, Methods: {route.methods}")


# def onStart():
#     for module_info in pkgutil.iter_modules([str(package_dir)]):
#         module = importlib.import_module(f'{module_info.name}')#routers.
#         print(module_info.name)
#         # print(hasattr(module, 'router'))
#         if hasattr(module, 'router'):
#             print(f'Including router from module: {module_info.name}', module.router)
#             app.include_router(module.router, prefix="/api")
#     print("Registered Routes:")
#     for route in app.routes:
#         print(f"Path: {route.path}, Methods: {route.methods}")

@app.get("/")
def read_root():
    return {"message": "Hello from EC2!"}


@app.get("/test")
def test():
    return {"message": "Hello from EC2!"}


@app.post("/strategic-model")
def strategicModel():
    # with resources.path(
    #     "pareto.case_studies",
    #     "strategic_toy_case_study.xlsx",
    # ) as fpath:
    #     [df_sets, df_parameters] = get_data(fpath, model_type="strategic")
    # strategic_model = create_model(
    #     df_sets,
    #     df_parameters,
    #     default={
    #         "objective": Objectives.cost,
    #         "pipeline_cost": PipelineCost.distance_based,
    #         "pipeline_capacity": PipelineCapacity.input,
    #         "hydraulics": Hydraulics.false,
    #         "desalination_model": DesalinationModel.false,
    #         "node_capacity": True,
    #         "water_quality": WaterQuality.false,
    #         "removal_efficiency_method": RemovalEfficiencyMethod.concentration_based,
    #         "infrastructure_timing": InfrastructureTiming.true,
    #         "subsurface_risk": SubsurfaceRisk.false,
    #     },
    # )
    # options = {
    #     "deactivate_slacks": True,
    #     "scale_model": False,
    #     "scaling_factor": 1000,
    #     "running_time": 200,
    #     "gap": 0,
    # }

    # results = solve_model(model=strategic_model, options=options)

    # with nostdout():
    #     feasibility_status = is_feasible(strategic_model)

    # if not feasibility_status:
    #     print("\nModel results are not feasible and should not be trusted\n" + "-" * 60)
    # else:
    #     print("\nModel results validated and found to pass feasibility tests\n" + "-" * 60)
    # print("\nConverting to Output Units and Displaying Solution\n" + "-" * 60)
        
    # [model, results_dict] = generate_report(
    #     strategic_model,
    #     results_obj=results,
    #     is_print=PrintValues.essential,
    #     output_units=OutputUnits.user_units,
    #     fname="strategic_optimization_results.xlsx",
    # )
    # pos = {
    #     "PP01": (20, 20),
    #     "PP02": (45, 20),
    #     "PP03": (50, 50),
    #     "PP04": (80, 40),
    #     "CP01": (65, 20),
    #     "F01": (75, 15),
    #     "F02": (75, 25),
    #     "K01": (30, 10),
    #     "K02": (40, 50),
    #     "S02": (60, 50),
    #     "S03": (10, 44),
    #     "S04": (10, 36),
    #     "R01": (20, 40),
    #     "R02": (70, 50),
    #     "O01": (1, 55),
    #     "O02": (1, 40),
    #     "O03": (1, 25),
    #     "N01": (30, 20),
    #     "N02": (30, 30),
    #     "N03": (30, 40),
    #     "N04": (40, 40),
    #     "N05": (45, 30),
    #     "N06": (50, 40),
    #     "N07": (60, 40),
    #     "N08": (60, 30),
    #     "N09": (70, 40),
    # }
    # plot_network(
    #     strategic_model,
    #     show_piping=True,
    #     show_trucking=True,
    #     show_results=False,
    #     save_fig="network.png",
    #     pos=pos,
    # )
    return {"message": "Success"}


# @app.post("/operational-model")
# def operationalModel():
#     set_list = [
#         "ProductionPads",
#         "CompletionsPads",
#         "ProductionTanks",
#         "ExternalWaterSources",
#         "WaterQualityComponents",
#         "StorageSites",
#         "SWDSites",
#         "TreatmentSites",
#         "ReuseOptions",
#         "NetworkNodes",
#     ]
#     parameter_list = [
#         "Units",
#         "RCA",
#         "FCA",
#         "PCT",
#         "FCT",
#         "CCT",
#         "PKT",
#         "PRT",
#         "CKT",
#         "CRT",
#         "PAL",
#         "CompletionsDemand",
#         "PadRates",
#         "TankFlowbackRates",
#         "FlowbackRates",
#         "ProductionTankCapacity",
#         "DisposalCapacity",
#         "CompletionsPadStorage",
#         "TreatmentCapacity",
#         "ExtWaterSourcingAvailability",
#         "PadOffloadingCapacity",
#         "TruckingTime",
#         "DisposalOperationalCost",
#         "TreatmentOperationalCost",
#         "ReuseOperationalCost",
#         "PadStorageCost",
#         "PipelineOperationalCost",
#         "TruckingHourlyCost",
#         "ExternalSourcingCost",
#         "ProductionRates",
#         "TreatmentEfficiency",
#         "ExternalWaterQuality",
#         "PadWaterQuality",
#         "StorageInitialWaterQuality",
#     ]
#     with resources.path(
#         "pareto.case_studies", "operational_generic_case_study.xlsx"
#     ) as fpath:
#         [df_sets, df_parameters] = get_data(fpath, set_list, parameter_list)
#     # Additional input data
#     df_parameters["MinTruckFlow"] = 0  # barrels/day
#     df_parameters["MaxTruckFlow"] = 259000  # barrels/day
#     operational_model = create_model(
#         df_sets,
#         df_parameters,
#         default={
#             "has_pipeline_constraints": True,
#             "production_tanks": ProdTank.equalized,
#             "water_quality": WaterQuality.false,
#         },
#     )
#     opt = get_solver("gurobi_direct", "gurobi", "cbc")
#     set_timeout(opt, timeout_s=60)
#     results = opt.solve(operational_model, tee=True)
#     results.write()
#     with nostdout():
#         feasibility_status = is_feasible(operational_model)
#     if not feasibility_status:
#         print("\nModel results are not feasible and should not be trusted\n" + "-" * 60)
#     else:
#         print("\nModel results validated and found to pass feasibility tests\n" + "-" * 60)


#     if operational_model.config.water_quality is WaterQuality.post_process:
#         operational_model = postprocess_water_quality_calculation(
#             operational_model, df_sets, df_parameters, opt
#         )
#     [model, results_dict] = generate_report(
#         operational_model,
#         is_print=PrintValues.essential,
#         output_units=OutputUnits.user_units,
#         fname="PARETO_report.xlsx",
#     )
#     set_list = []
#     parameter_list = ["v_F_Trucked", "v_C_Trucked"]
#     fname = "PARETO_report.xlsx"
#     [sets_reports, parameters_report] = get_data(fname, set_list, parameter_list)
#     file_path = "PARETO_report.xlsx"

#     # Check if the file exists before serving it
#     if not os.path.exists(file_path):
#         return {"error": "Report file not found!"}
#     return FileResponse(
#         path=file_path,
#         filename="PARETO_report.xlsx",
#         media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#     )

@app.get("/download-report", response_class=FileResponse)
def download_report():
    """ Endpoint to download the generated report file """
    file_path = "PARETO_report.xlsx"

    # Check if the file exists before serving it
    if not os.path.exists(file_path):
        return {"error": "Report file not found!"}

    return FileResponse(
        path=file_path,
        filename="PARETO_report.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
