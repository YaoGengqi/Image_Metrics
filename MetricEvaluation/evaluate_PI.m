%% Parameters
% Directory with your results
%%% Make sure the file names are as exactly %%%
%%% as the original ground truth images %%%

function res = evaluate_PI(input_dir, test_name)

verbose = true;
shave_width = 4;

%% Calculate scores and save
addpath('MetricEvaluation\utils');

scores = calc_PI(input_dir, verbose);

%% Printing results
res = (mean([scores.NIQE]) + (10 - mean([scores.Ma]))) / 2;
fprintf(['The PI of ', input_dir, ' is: ', num2str(res)]);
fprintf(['The PI of ', input_dir, ' is: ', num2str(mean([scores.PI]))])
end
