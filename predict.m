function [bias, stdev,y_hat_reg] = predict(regressor,X_test,y_test)
y_hat_reg = regressor.predictFcn(X_test);

errors = y_hat_reg-y_test;
bias = mean(errors);
stdev = std(errors);
disp("Prediction bias: "+bias);
disp("Prediction standard deviation: "+stdev);
disp("");
disp("");

%figure
%histfit(errors);
%xlabel("Position error")
%ylabel("Number of test samples")
%pos_list = unique(y_test);
%num_pos = length(pos_list);
%pos_step = pos_list(2)-pos_list(1);
%x_tick_nums = pos_step*(-num_pos:1:num_pos);
%xticks(x_tick_nums)
%xticklabels(string(x_tick_nums));

end