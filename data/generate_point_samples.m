n = 1000000;
samples = 2 * (rand(n, 3) - 0.5);
dlmwrite('point_sample_in.txt', samples, ' ');
