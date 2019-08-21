close all
clear all
clc
% %%
% 
% files = dir('*.txt');
% arrays = {};
% labels = {};
% for i=1:1:length(files)
%     %eval(['load ' files(i).name ' -ascii']);
%     fname = files(i).name;
%     table_data = importfile(fname);
%     arr = table2array(table_data);
%     split_str = split(fname,'_');
%     label = str2double(cell2mat(split_str(2)));
%     arr = arr';
%     labels{i} = label*ones(size(arr(1,:)));
%     arrays{i} = arr;
% end
% Xs = cell2mat(arrays);
% Xs = Xs';
% ys = cell2mat(labels);
% ys = ys';
% data = [Xs,ys];
% N = length(data);
% num_classes = length(unique(ys));
% clear arr arrays label labels table_data Xs split_str i fname files 
%%
importfile(uigetfile);
N = length(data);
Xs = data(:,1:3);
y_1 = data(:,4);
y_2 = data(:,5);
ys = [y_1,y_2];
%%
acc_array = {};
j=1;
% for class_portion = [1,1/2,1/4,1/8]% 0.125 -1 . Values lower than 0.125 will yield 2 classes: 0, and 1 other depending on the exact value
%     for train_portion = [0.8,0.1] %    0.1 - 0.99
class_portion = 1;
train_portion = 0.8;
%% Change training type
selection_type = ["even","random","blind"];
class_selection = selection_type(1);
%% Train-test split
shuffled = data(randperm(N),:);
train_test_cutoff = floor(N*train_portion);
train_data = shuffled(1:train_test_cutoff-1,:);
test_data = shuffled(train_test_cutoff:end,:);

%% Class dropout
y_train = train_data(:,4);
y_test = test_data(:,4);
if strcmp(class_selection,"even") == 1
    divisor = 64*ceil(1/(class_portion));
    train_idx = mod(y_train,divisor)==0;
    %test_idx = mod(ys,divisor)~=0;
else
    if strcmp(class_selection,"random")==1
    classes = unique(y_train);
    shuffled_classes = classes(randperm(length(classes)));
    train_classes = shuffled_classes(1:length(classes)*class_portion);
    train_idx = ismember(y_train,train_classes);
    %test_idx = ~ismember(ys,train_classes);
    
    else 
        if strcmp(class_selection,"blind")
            divisor = 64*ceil(1/(class_portion));
            train_idx = mod(y_train,divisor)==0;
            test_idx = mod(y_test,divisor)~=0;
            test_data = test_data(test_idx,:);

        end
    end
    
end

train_data = train_data(train_idx,:);

%% Split X and Y's
y_train = train_data(:,4:5);
y_test = test_data(:,4:5);
X_train = train_data(:,1:3);
X_test = test_data(:,1:3);

true_train_portion = length(X_train)/N;
true_class_portion = length(unique(train_data(:,end)))/length(unique(ys));
disp("Trained on "+true_train_portion*100+"% of the data,  sampled from "+...
        floor(true_class_portion*num_classes)+"/"+num_classes+" classes.");
%% Regression
disp("================Regression=================");
[regressor, valid_rmse] = trainRegressionModel(train_data);%Regenerate these functions using the learner apps, whenever making changes to code
y_hat_reg = regressor.predictFcn(test_data(:,1:3));
errors = y_hat_reg-y_test;
bias = mean(errors);
stdev = std(errors);
figure
histfit(errors);
xlabel("Position error")
ylabel("Number of test samples")
title("Distribution of errors for position classification")
disp("Prediction bias: "+bias);
disp("Prediction standard deviation: "+stdev);
disp("")

%% Classification: Not useful for generalizations
if 0
disp("==============Classification===============");
[classifier, valid_acc] = trainClassifier(train_data);%Regenerate these functions using the learner apps, whenever making changes to code
y_hat_class = classifier.predictFcn(test_data(:,1:3));
correct = y_test==y_hat_class;
acc = sum(correct)/length(test_data);
figure
confusionchart(confusionmat(y_test,y_hat_class),unique(ys));
title("Confusion matrix for position classification")
disp("Prediction accuracy: "+100*acc+"%");
acc_array{j}= acc;
j=j+1;
end

