bazel build -c opt \
--define MEDIAPIPE_DISABLE_GPU=1 \
--define no_aws_support=true \
${1-predict_mp}
