from rvc_python.infer import RVCInference

rvc = RVCInference(
    device="cuda:0",
    model_path="resources/voice_models/narrator/LenvalBrown50m300e.pth",
    index_path="resources/voice_models/narrator/added_IVF3842_Flat_nprobe_1_LenvalBrown50m300e_v2.index",
    version="v2"
    )

rvc.set_params(index_rate=0.2)