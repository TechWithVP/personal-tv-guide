import random
import os

import modules.shield
import modules.html
import modules.runtime
import modules.genre

from dotenv import load_dotenv

# Variables
load_dotenv()
when_to_start = int(os.environ.get('WHEN_TO_START')) # first hour in output table
hours_to_print = int(os.environ.get('HOURS_TO_PRINT')) # how many hours worth of data in table
outfile = str(os.environ.get('OUTFILE'))


# Restore my work
import modules.data_bin_convert
# modules.data_bin_convert.data_to_bin(data_tuples)
data_tuples_movies = modules.data_bin_convert.bin_to_data('./saved_data_movies.bin')
# data_tuples_tv = modules.data_bin_convert.bin_to_data('./saved_data_tv.bin')
# all_genres = modules.data_bin_convert.bin_to_data('./saved_data_genres.bin')

# data_tuples = data_tuples_movies + data_tuples_tv
data_tuples = data_tuples_movies


# # Randomize the lists
# random.shuffle(data_tuples)
# random.shuffle(all_genres)


# Sort by runtime
# def get_runtime_minutes(element):
#     return modules.runtime.runtime_to_minutes(element[5],False)

# lambda x:(modules.runtime.runtime_to_minutes(x[5]))
data_tuples = sorted(data_tuples,key=lambda x:(modules.runtime.runtime_to_minutes(x[5],False)))
# data_tuples.sort(reverse=False,key=get_runtime_minutes)

# # Look through data for keyword matches
# use_keyword_lists = True # TODO: move to .env file
# genre_triggers, remainder = modules.genre.split_by_keyword(data_tuples,modules.genre.trigger_keywords())
# genre_christmas, remainder = modules.genre.split_by_keyword(remainder,modules.genre.christmas_keywords())


# # Loop through all_genres to separate data by genre
# i = 0
# genre_lists = []
# if not use_keyword_lists:
#     remainder = data_tuples
# while len(remainder) > 0:
#     list_with_genre, remainder = modules.genre.split_by_genre(remainder, all_genres[i])
#     genre_lists.append(list_with_genre)
#     i += 1


# Begin writing data
html_handle = open(outfile,'+w')
html_handle.write(modules.html.generate_html_start())
# html_handle.write(modules.html.generate_table_th(when_to_start,hours_to_print))


# # Write table rows for keyword lists
# if use_keyword_lists:
#     html_handle.write(modules.html.generate_html_genre_tds(genre_triggers,'Trigger Warning',hours_to_print))
#     html_handle.write(modules.html.generate_html_genre_tds(genre_christmas,'Christmas',hours_to_print))


# # Write table rows for looped genre_lists
# for i in range(len(genre_lists)):
#     if genre_lists[i]:
#         html_handle.write(modules.html.generate_html_genre_tds(genre_lists[i], all_genres[i], hours_to_print))

headers_list = ['Title','Runtime']

html_handle.write(modules.html.sort_by_runtime_table_header(headers_list))

for i in range(len(data_tuples)):
    shield = modules.shield.generate_shield(data_tuples[i])
    runtime_str = str(modules.runtime.runtime_to_minutes(data_tuples[i][5],False))
    title_and_runtime_list = [shield,runtime_str]
    html_handle.write(modules.html.sort_by_runtime_table_row(title_and_runtime_list))


# Finish writing data
html_handle.write(modules.html.generate_html_end())
html_handle.close()
