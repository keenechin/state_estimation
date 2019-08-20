function [bias, stdev,y_hat_reg] = predict(regressor,X_test,y_test)

y_hat_reg = regressor.predictFcn(X_test);
errors = y_hat_reg-y_test;
err_dist = mean(errors,2);
bias = mean(err_dist);
stdev = std(err_dist);
figure
histfit(err_dist);
xlabel("Position error")
ylabel("Number of test samples")
title("Distribution of errors for position classification")
disp("Prediction bias: "+bias);
disp("Prediction standard deviation: "+stdev);
disp("")
end