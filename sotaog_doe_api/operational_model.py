
import fastapi
from fastapi.responses import FileResponse
from pareto.operational_water_management.operational_produced_water_optimization_model import (
    WaterQuality,
    create_model,
    ProdTank,
    postprocess_water_quality_calculation,
)
from pareto.utilities.get_data import get_data
from pareto.utilities.results import (
    generate_report,
    PrintValues,
    OutputUnits,
    is_feasible,
    nostdout,
)
from pareto.utilities.solvers import get_solver, set_timeout
from importlib import resources
import pandas as pd
import os

router = fastapi.APIRouter(prefix='/pareto',  tags=['Pareto'])
router.post("/operational-model")
async def operational_model():
    set_list = [
        "ProductionPads",
        "CompletionsPads",
        "ProductionTanks",
        "ExternalWaterSources",
        "WaterQualityComponents",
        "StorageSites",
        "SWDSites",
        "TreatmentSites",
        "ReuseOptions",
        "NetworkNodes",
    ]
    parameter_list = [
        "Units",
        "RCA",
        "FCA",
        "PCT",
        "FCT",
        "CCT",
        "PKT",
        "PRT",
        "CKT",
        "CRT",
        "PAL",
        "CompletionsDemand",
        "PadRates",
        "TankFlowbackRates",
        "FlowbackRates",
        "ProductionTankCapacity",
        "DisposalCapacity",
        "CompletionsPadStorage",
        "TreatmentCapacity",
        "ExtWaterSourcingAvailability",
        "PadOffloadingCapacity",
        "TruckingTime",
        "DisposalOperationalCost",
        "TreatmentOperationalCost",
        "ReuseOperationalCost",
        "PadStorageCost",
        "PipelineOperationalCost",
        "TruckingHourlyCost",
        "ExternalSourcingCost",
        "ProductionRates",
        "TreatmentEfficiency",
        "ExternalWaterQuality",
        "PadWaterQuality",
        "StorageInitialWaterQuality",
    ]
    with resources.path(
        "pareto.case_studies", "operational_generic_case_study.xlsx"
    ) as fpath:
        [df_sets, df_parameters] = get_data(fpath, set_list, parameter_list)
    # Additional input data
    df_parameters["MinTruckFlow"] = 0  # barrels/day
    df_parameters["MaxTruckFlow"] = 259000  # barrels/day
    operational_model = create_model(
        df_sets,
        df_parameters,
        default={
            "has_pipeline_constraints": True,
            "production_tanks": ProdTank.equalized,
            "water_quality": WaterQuality.false,
        },
    )
    opt = get_solver("gurobi_direct", "gurobi", "cbc")
    set_timeout(opt, timeout_s=60)
    results = opt.solve(operational_model, tee=True)
    results.write()
    with nostdout():
        feasibility_status = is_feasible(operational_model)
    if not feasibility_status:
        print("\nModel results are not feasible and should not be trusted\n" + "-" * 60)
    else:
        print("\nModel results validated and found to pass feasibility tests\n" + "-" * 60)


    if operational_model.config.water_quality is WaterQuality.post_process:
        operational_model = postprocess_water_quality_calculation(
            operational_model, df_sets, df_parameters, opt
        )
    [model, results_dict] = generate_report(
        operational_model,
        is_print=PrintValues.essential,
        output_units=OutputUnits.user_units,
        fname="PARETO_report.xlsx",
    )
    set_list = []
    parameter_list = ["v_F_Trucked", "v_C_Trucked"]
    fname = "PARETO_report.xlsx"
    [sets_reports, parameters_report] = get_data(fname, set_list, parameter_list)
    file_path = "PARETO_report.xlsx"

    # Check if the file exists before serving it
    if not os.path.exists(file_path):
        return {"error": "Report file not found!"}
    return FileResponse(
        path=file_path,
        filename="PARETO_report.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )