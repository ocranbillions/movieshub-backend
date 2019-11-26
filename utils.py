def validate_movie(movie):
    if (movie.title == '' or movie.release_year == ''):
        return False
    else:
        return True
