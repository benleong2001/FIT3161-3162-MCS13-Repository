	9��@9��@!9��@	�Bc�!@�Bc�!@!�Bc�!@"{
=type.googleapis.com/tensorflow.profiler.PerGenericStepDetails:9��@���s��?A�E&��H�?Y<P�<��?rEagerKernelExecute 0*	rh��|�q@2U
Iterator::Model::ParallelMapV2������?!�1�JA@)������?1�1�JA@:Preprocessing2l
5Iterator::Model::ParallelMapV2::Zip[1]::ForeverRepeat^���4�?!��R��;6@)���M�?1���2@:Preprocessing2F
Iterator::Model3�`����?!�U�6��I@)�!�Q*�?1�G����1@:Preprocessing2f
/Iterator::Model::ParallelMapV2::Zip[0]::FlatMap�Ws�`��?!�H�
�4@)���/fK�?1n��c�.@:Preprocessing2v
?Iterator::Model::ParallelMapV2::Zip[0]::FlatMap[0]::TensorSlice�,'��?!�G��`�@)�,'��?1�G��`�@:Preprocessing2Z
#Iterator::Model::ParallelMapV2::Zip��#���?!y�w�RH@)�f+/���?1[)f��@:Preprocessing2x
AIterator::Model::ParallelMapV2::Zip[1]::ForeverRepeat::FromTensor	��Ln�?!N�%��@)	��Ln�?1N�%��@:Preprocessing:�
]Enqueuing data: you may want to combine small input data chunks into fewer but larger chunks.
�Data preprocessing: you may increase num_parallel_calls in <a href="https://www.tensorflow.org/api_docs/python/tf/data/Dataset#map" target="_blank">Dataset map()</a> or preprocess the data OFFLINE.
�Reading data from files in advance: you may tune parameters in the following tf.data API (<a href="https://www.tensorflow.org/api_docs/python/tf/data/Dataset#prefetch" target="_blank">prefetch size</a>, <a href="https://www.tensorflow.org/api_docs/python/tf/data/Dataset#interleave" target="_blank">interleave cycle_length</a>, <a href="https://www.tensorflow.org/api_docs/python/tf/data/TFRecordDataset#class_tfrecorddataset" target="_blank">reader buffer_size</a>)
�Reading data from files on demand: you should read data IN ADVANCE using the following tf.data API (<a href="https://www.tensorflow.org/api_docs/python/tf/data/Dataset#prefetch" target="_blank">prefetch</a>, <a href="https://www.tensorflow.org/api_docs/python/tf/data/Dataset#interleave" target="_blank">interleave</a>, <a href="https://www.tensorflow.org/api_docs/python/tf/data/TFRecordDataset#class_tfrecorddataset" target="_blank">reader buffer</a>)
�Other data reading or processing: you may consider using the <a href="https://www.tensorflow.org/programmers_guide/datasets" target="_blank">tf.data API</a> (if you are not using it now)�
:type.googleapis.com/tensorflow.profiler.BottleneckAnalysis�
both�Your program is MODERATELY input-bound because 9.0% of the total step time sampled is waiting for input. Therefore, you would need to reduce both the input time and other time.no*moderate2t10.8 % of the total step time sampled is spent on 'All Others' time. This could be due to Python execution overhead.9�Bc�!@Ip���3�V@Zno>Look at Section 3 for the breakdown of input time on the host.B�
@type.googleapis.com/tensorflow.profiler.GenericStepTimeBreakdown�
	���s��?���s��?!���s��?      ��!       "      ��!       *      ��!       2	�E&��H�?�E&��H�?!�E&��H�?:      ��!       B      ��!       J	<P�<��?<P�<��?!<P�<��?R      ��!       Z	<P�<��?<P�<��?!<P�<��?b      ��!       JCPU_ONLYY�Bc�!@b qp���3�V@