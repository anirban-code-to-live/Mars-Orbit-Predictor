import os
import pandas as pd
import numpy as np
import math
import sys
import FirstProblem as fp
import SecondProblem as sp
import ThirdProblem as tp
import FourthProblem as fp

if __name__ == '__main__':
    mars_opposition_data = pd.read_csv('../data/01_data_mars_opposition.csv')
    # print(mars_opposition_data.values.shape)
    mars_heliocentric_longitude = mars_opposition_data.values[:, 3:7]
    # print(mars_heliocentric_longitude.shape)
    mars_mean_longitude = mars_opposition_data.values[:, 9:13]
    # print(mars_mean_longitude.shape)
    mars_heliocentric_longitude_in_degree = mars_heliocentric_longitude[:, 0:1] * 30 + \
                                            mars_heliocentric_longitude[:, 1:2] + \
                                            mars_heliocentric_longitude[:, 2:3] / 60.0 + \
                                            mars_heliocentric_longitude[:, 3:4] / 3600.0
    mars_heliocentric_longitude_in_rad = mars_heliocentric_longitude_in_degree * math.pi / 180.0
    # print(mars_heliocentric_longitude_in_degree)
    # print(mars_heliocentric_longitude_in_rad)
    mars_mean_longitude_in_degree = mars_mean_longitude[:, 0:1] * 30 + \
                                    mars_mean_longitude[:, 1:2] + \
                                    mars_mean_longitude[:, 2:3] / 60.0 + \
                                    mars_mean_longitude[:, 3:4] / 3600.0
    mars_mean_longitude_in_rad = mars_mean_longitude_in_degree * math.pi / 180.0
    # print(mars_mean_longitude_in_degree)
    # print(mars_mean_longitude_in_rad)
    mars_geocentric_latitude = mars_opposition_data.values[:, 7:9]
    mars_geocentric_latitude_in_radian = (math.pi / 180.0) * (mars_geocentric_latitude[:, 0:1] +
                                                            mars_geocentric_latitude[:, 1:2] / 60.0)
    # print mars_geocentric_latitude
    # print mars_geocentric_latitude_in_radian
    #
    # # Solution for first problem
    #
    # print 'Loss function :: log(arithmetic mean) - log(geometric mean)'
    # print 'Initial guess of x :: 1.2'
    # print 'Initial guess of y :: 0.2'
    # first_problem = fp.FirstProblem([1.2, 0.2],
    #                              mars_mean_longitude_in_rad,
    #                              mars_heliocentric_longitude_in_rad)
    # x, y = first_problem.minimize_loss_function(0)
    # print "Optimized parameter values :: " + 'x  = ' + str(x) + ' and y = ' + str(y)
    # print 'Radius and angle(in degree) pair w.r.t. reference line'
    # for index in range(mars_heliocentric_longitude_in_rad.shape[0]):
    #     phi, radius = first_problem.get_angular_position_and_radius_of_mars(x, y,
    #                                                                       mars_mean_longitude_in_rad[index],
    #                                                                       mars_heliocentric_longitude_in_rad[index])
    #     print radius, phi*180/math.pi
    #
    # print 'Loss function :: sample variance'
    # print 'Initial guess of x :: 1.2'
    # print 'Initial guess of y :: 0.2'
    # first_problem = fp.FirstProblem([1.2, 0.2],
    #                              mars_mean_longitude_in_rad,
    #                              mars_heliocentric_longitude_in_rad)
    # x, y = first_problem.minimize_loss_function(1)
    # print "Optimized parameter values :: " + 'x  = ' + str(x) + ' and y = ' + str(y)
    # print 'Radius and angle(in degree) pair w.r.t. reference line'
    # for index in range(mars_heliocentric_longitude_in_rad.shape[0]):
    #     phi, radius = first_problem.get_angular_position_and_radius_of_mars(x, y,
    #                                                                       mars_mean_longitude_in_rad[index],
    #                                                                       mars_heliocentric_longitude_in_rad[index])
    #     print radius, phi*180/math.pi

    triangulation_data = pd.read_csv('../data/01_data_mars_triangulation.csv')
    triangulation_index_pair = triangulation_data.values[:, 0:1]
    triangulation_observation_time = triangulation_data.values[:, 1:4]
    triangulation_earth_heliocentric_longitude = triangulation_data.values[:, 4:6]
    triangulation_mars_geocentric_longitude = triangulation_data.values[:, 6:8]

    # print triangulation_earth_heliocentric_longitude
    # print triangulation_mars_geocentric_longitude

    triangulation_earth_heliocentric_longitude_in_radian = (math.pi / 180.0) * (
                triangulation_earth_heliocentric_longitude[:, 0:1] +
                triangulation_earth_heliocentric_longitude[:, 1:2] / 60.0)

    triangulation_mars_geocentric_longitude_in_radian = (math.pi / 180.0) * (
                triangulation_mars_geocentric_longitude[:, 0:1] +
                triangulation_mars_geocentric_longitude[:, 1:2] / 60.0)
    # print triangulation_earth_heliocentric_longitude_in_radian
    # print triangulation_mars_geocentric_longitude_in_radian

    # Solution for second problem
    print'\nSecond Problem >>>'
    second_problem = sp.SecondProblem(triangulation_index_pair,
                                      triangulation_earth_heliocentric_longitude_in_radian,
                                      triangulation_mars_geocentric_longitude_in_radian)
    mars_triangulation_radius, mars_triangulation_angular_pos = second_problem.find_mars_projection_on_ecliptic_plane()
    print 'Five different projections of Mars\'s location on the ecliptic plane :: '
    print mars_triangulation_radius, mars_triangulation_angular_pos
    mars_orbit_radius = second_problem.fit_circle_for_mars_orbit([1])
    print 'Mars orbital radius(best fit circle centered on sun:: '
    print mars_orbit_radius

    # Solution for third problem
    print'\nThird Problem >>>'
    third_problem = tp.ThirdProblem(mars_heliocentric_longitude_in_rad)
    mars_heliocentric_latitude_in_degree = third_problem.find_mars_heliocentric_latitude(mars_geocentric_latitude_in_radian,
                                                                               mars_orbit_radius)
    print 'Mars heliocentric latitude(in degree) :: '
    print mars_heliocentric_latitude_in_degree
    mars_orbital_inclination_in_radian = third_problem.fit_circle_for_mars_orbit([0.1])
    mars_orbital_inclination_in_degree = mars_orbital_inclination_in_radian * (180.0/math.pi)
    print 'Mars orbital inclination(in degree) with ecliptic plane:: '
    print mars_orbital_inclination_in_degree

    # Solution for fourth problem
    print'\nFourth Problem >>>'
    fourth_problem = fp.FourthProblem(mars_triangulation_radius, mars_orbital_inclination_in_radian[0])
    mars_triangulated_radius_orbital_plane = fourth_problem.find_mars_3d_location_in_orbital_plane()
    print 'Mars\'s five different (3-d) locations on Mars\'s orbital plane :: '
    print mars_triangulated_radius_orbital_plane
    mars_best_fit_circular_radius, total_loss_circular_fit = fourth_problem.fit_circle_to_mars_orbital_plane([1.5])
    print 'Best fit circle on Mars\'s orbital plane with the Sun as centre :: '
    print mars_best_fit_circular_radius
    print 'Sum of losses for circular orbit :: '
    print total_loss_circular_fit


