cc_binary(
    name = "extract_mp",
    srcs = ["extract_mp.cc"],
    deps = [
        "@com_google_absl//absl/strings",
        "//mediapipe/framework:calculator_framework",
        "//mediapipe/framework/formats:matrix",
        "//mediapipe/framework/formats:matrix_data_cc_proto",
        "//mediapipe/framework/port:commandlineflags",
        "//mediapipe/framework/port:file_helpers",
        "//mediapipe/framework/port:map_util",
        "//mediapipe/framework/port:parse_text_proto",
        "//mediapipe/framework/port:status",
        "//mediapipe/graphs/youtube8m:yt8m_feature_extraction_calculators",
        "@org_tensorflow//tensorflow/core:all_kernels",
        "@org_tensorflow//tensorflow/core:direct_session",
    ],
)

cc_binary(
    name = "predict_mp",
    deps = [
        "//mediapipe/examples/desktop:simple_run_graph_main",
        "//mediapipe/graphs/youtube8m:yt8m_inference_calculators_deps",
        "@org_tensorflow//tensorflow/core:all_kernels",
        "@org_tensorflow//tensorflow/core:direct_session",
    ],
)
