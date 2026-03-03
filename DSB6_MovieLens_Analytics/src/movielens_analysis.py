import csv
from collections import defaultdict


def file_reader(filename):
    """
    Читает первые 1000 строк из CSV-файла и возвращает список словарей.
    """
    data = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                if i >= 1000:
                    break
                data.append(row)
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл не найден: {filename}")
    except Exception as e:
        raise RuntimeError(f"Ошибка при чтении файла {filename}: {e}")
    return data


class Ratings:
    """
    Работа с файлом ratings.csv: userId,movieId,rating,timestamp
    """
    
    def __init__(self, filepath):
        self.ratings = []
        self.user_ratings = defaultdict(list)
        self.movie_ratings = defaultdict(list)
        self._load_data(filepath)

    def _load_data(self, filepath):
        try:
            rows = file_reader(filepath)
            for row in rows:
                try:
                    user_id = int(row['userId'])
                    movie_id = int(row['movieId'])
                    rating = float(row['rating'])
                    timestamp = int(row['timestamp'])
                    entry = {'userId': user_id, 'movieId': movie_id, 'rating': rating, 'timestamp': timestamp}
                    self.ratings.append(entry)
                    self.user_ratings[user_id].append(entry)
                    self.movie_ratings[movie_id].append(entry)
                except (KeyError, ValueError):
                    continue
        except Exception as e:
            raise RuntimeError(f"Не удалось загрузить данные из {filepath}: {e}")

    def get_user_ratings(self, user_id):
        """
        Получить все рейтинги пользователя по его ID.
        Возвращает список словарей, отсортированный по времени (timestamp).
        """
        if not isinstance(user_id, int) or user_id <= 0:
            raise ValueError("user_id должен быть положительным целым числом")
        return sorted(self.user_ratings.get(user_id, []), key=lambda x: x['timestamp'])

    def get_movie_ratings(self, movie_id):
        """
        Получить все рейтинги фильма по его ID.
        Возвращает список словарей с рейтингами.
        """
        if not isinstance(movie_id, int) or movie_id <= 0:
            raise ValueError("movie_id должен быть положительным целым числом")
        return self.movie_ratings.get(movie_id, [])

    def get_top_rated_movies(self, n=10):
        """
        Получить топ-N фильмов по среднему рейтингу.
        Возвращает список кортежей: [(movieId, avg_rating, count), ...], 
        отсортированный по убыванию среднего рейтинга и количества оценок.
        """
        if not isinstance(n, int) or n <= 0:
            raise ValueError("n должен быть положительным целым числом")
        top = []
        for movie_id, ratings in self.movie_ratings.items():
            avg = sum(r['rating'] for r in ratings) / len(ratings)
            top.append((movie_id, round(avg, 2), len(ratings)))
        return sorted(top, key=lambda x: (-x[1], -x[2]))[:n]

    def get_rating_distribution(self):
        """
        Получить распределение оценок по значениям.
        Возвращает список кортежей: [(оценка, количество), ...], 
        отсортированный по возрастанию оценки.
        """
        dist = defaultdict(int)
        for r in self.ratings:
            dist[r['rating']] += 1
        return sorted(dist.items(), key=lambda x: x[0])

    def get_average_user_rating(self, user_id):
        """
        Получить средний рейтинг пользователя по его ID.
        Возвращает число с плавающей точкой (0.0, если пользователь не найден).
        """
        if not isinstance(user_id, int) or user_id <= 0:
            raise ValueError("user_id должен быть положительным целым числом")
        ratings = self.user_ratings.get(user_id, [])
        if not ratings:
            return 0.0
        return round(sum(r['rating'] for r in ratings) / len(ratings), 2)

    def get_ratings_count(self):
        """
        Получить общее количество рейтингов в датасете.
        Возвращает целое число.
        """
        return len(self.ratings)

    def get_users_count(self):
        """
        Получить количество уникальных пользователей с рейтингами.
        Возвращает целое число.
        """
        return len(self.user_ratings)


class Tags:
    """
    Работа с файлом tags.csv: userId,movieId,tag,timestamp
    """
    
    def __init__(self, filepath):
        self.tags = []
        self.movie_tags = defaultdict(list)
        self.user_tags = defaultdict(list)
        self.tag_frequency = defaultdict(int)
        self._load_data(filepath)

    def _load_data(self, filepath):
        try:
            rows = file_reader(filepath)
            for row in rows:
                try:
                    user_id = int(row['userId'])
                    movie_id = int(row['movieId'])
                    tag = row['tag'].lower().strip()
                    timestamp = int(row['timestamp'])
                    entry = {'userId': user_id, 'movieId': movie_id, 'tag': tag, 'timestamp': timestamp}
                    self.tags.append(entry)
                    self.movie_tags[movie_id].append(entry)
                    self.user_tags[user_id].append(entry)
                    self.tag_frequency[tag] += 1
                except (KeyError, ValueError):
                    continue
        except Exception as e:
            raise RuntimeError(f"Не удалось загрузить данные из {filepath}: {e}")

    def get_movie_tags(self, movie_id):
        """
        Получить уникальные теги фильма по его ID.
        Возвращает отсортированный список строк (тегов).
        """
        if not isinstance(movie_id, int) or movie_id <= 0:
            raise ValueError("movie_id должен быть положительным целым числом")
        unique_tags = {t['tag'] for t in self.movie_tags.get(movie_id, [])}
        return sorted(unique_tags)

    def get_user_tags(self, user_id):
        """
        Получить уникальные теги пользователя по его ID.
        Возвращает отсортированный список строк (тегов).
        """
        if not isinstance(user_id, int) or user_id <= 0:
            raise ValueError("user_id должен быть положительным целым числом")
        unique_tags = {t['tag'] for t in self.user_tags.get(user_id, [])}
        return sorted(unique_tags)

    def get_popular_tags(self, n=10):
        """
        Получить топ-N самых популярных тегов.
        Возвращает список кортежей: [(тег, количество), ...], 
        отсортированный по убыванию частоты и алфавиту.
        """
        if not isinstance(n, int) or n <= 0:
            raise ValueError("n должен быть положительным целым числом")
        popular = [(tag, count) for tag, count in self.tag_frequency.items()]
        return sorted(popular, key=lambda x: (-x[1], x[0]))[:n]

    def get_all_tags_count(self):
        """
        Получить общее количество применённых тегов (с повторениями).
        Возвращает целое число.
        """
        return len(self.tags)

    def get_unique_tags_count(self):
        """
        Получить количество уникальных тегов в датасете.
        Возвращает целое число.
        """
        return len(self.tag_frequency)


class Links:
    """
    Работа с файлом links.csv: movieId,imdbId,tmdbId
    """
    
    def __init__(self, filepath):
        self.links = {}
        self._load_data(filepath)

    def _load_data(self, filepath):
        try:
            rows = file_reader(filepath)
            for row in rows:
                try:
                    movie_id = int(row['movieId'])
                    imdb_id = int(row['imdbId']) if row['imdbId'] else None
                    tmdb_id = int(row['tmdbId']) if row['tmdbId'] else None
                    self.links[movie_id] = {'imdbId': imdb_id, 'tmdbId': tmdb_id}
                except (KeyError, ValueError):
                    continue
        except Exception as e:
            raise RuntimeError(f"Не удалось загрузить данные из {filepath}: {e}")

    def get_imdb_id(self, movie_id):
        """
        Получить IMDb ID фильма по movieId.
        Возвращает целое число (0, если фильм не найден или ID отсутствует).
        """
        if not isinstance(movie_id, int) or movie_id <= 0:
            raise ValueError("movie_id должен быть положительным целым числом")
        return self.links.get(movie_id, {}).get('imdbId', 0)

    def get_tmdb_id(self, movie_id):
        """
        Получить TMDb ID фильма по movieId.
        Возвращает целое число (0, если фильм не найден или ID отсутствует).
        """
        if not isinstance(movie_id, int) or movie_id <= 0:
            raise ValueError("movie_id должен быть положительным целым числом")
        return self.links.get(movie_id, {}).get('tmdbId', 0)

    def get_all_linked_movies(self):
        """
        Получить список всех movieId, для которых есть внешние ссылки.
        Возвращает отсортированный список целых чисел.
        """
        return sorted(self.links.keys())

    def get_links_count(self):
        """
        Получить количество фильмов со внешними ссылками.
        Возвращает целое число.
        """
        return len(self.links)


class Movies:
    """
    Работа с файлом movies.csv: movieId,title,genres
    """
    
    def __init__(self, filepath):
        self.movies = {}
        self.genres_index = defaultdict(list)
        self._load_data(filepath)
    
    def _load_data(self, filepath):
        try:
            rows = file_reader(filepath)
            for row in rows:
                try:
                    movie_id = int(row['movieId'])
                    title = row['title']
                    genres = row['genres'].split('|') if row['genres'] != '(no genres listed)' else []
                    self.movies[movie_id] = {'title': title, 'genres': genres}
                    for genre in genres:
                        self.genres_index[genre].append(movie_id)
                except (KeyError, ValueError) as e:
                    continue
        except Exception as e:
            raise RuntimeError(f"Не удалось загрузить данные из {filepath}: {e}")
    
    def get_movie_info(self, movie_id):
        """
        Получить информацию о фильме по ID.
        Возвращает dict или пустой dict, если фильм не найден.
        """
        if not isinstance(movie_id, int):
            raise TypeError("movie_id должен быть целым числом")
        if movie_id <= 0:
            raise ValueError("movie_id должен быть положительным")
        return self.movies.get(movie_id, {})
    
    def get_movies_by_genre(self, genre):
        """
        Получить список movieId фильмов указанного жанра (отсортирован по возрастанию).
        """
        if not isinstance(genre, str):
            raise TypeError("genre должен быть строкой")
        if not genre.strip():
            raise ValueError("genre не может быть пустой строкой")
        return sorted(self.genres_index.get(genre, []))
    
    def get_genre_distribution(self):
        """
        Распределение фильмов по жанрам: [(жанр, количество), ...]
        Отсортировано по убыванию количества, затем по алфавиту.
        """
        distribution = [(genre, len(movies)) for genre, movies in self.genres_index.items()]
        return sorted(distribution, key=lambda x: (-x[1], x[0]))
    
    def get_all_movie_ids(self):
        """
        Получить все movieId из датасета (отсортирован по возрастанию).
        """
        return sorted(self.movies.keys())
    
    def get_movie_title(self, movie_id):
        """
        Получить название фильма по ID.
        Возвращает строку (пустую, если фильм не найден).
        """
        if not isinstance(movie_id, int):
            raise TypeError("movie_id должен быть целым числом")
        if movie_id <= 0:
            raise ValueError("movie_id должен быть положительным")
        return self.movies.get(movie_id, {}).get('title', '')
    
    def get_movies_count(self):
        """
        Количество фильмов в датасете.
        """
        return len(self.movies)
    
    def get_genres_list(self):
        """
        Список всех уникальных жанров (отсортирован по алфавиту).
        """
        return sorted(self.genres_index.keys())


class Test:
    """
    Тесты для всех классов: Movies, Ratings, Tags, Links.
    Проверяются типы возвращаемых значений, корректность сортировки и обработка исключений.
    """

    # Тесты для Movies
    
    def test_movies_get_movie_info_returns_dict(self):
        movies = Movies('../datasets/ml-latest-small/movies.csv')
        result = movies.get_movie_info(1)
        assert isinstance(result, dict)

    def test_movies_get_movie_info_contains_title_and_genres(self):
        movies = Movies('../datasets/ml-latest-small/movies.csv')
        result = movies.get_movie_info(1)
        assert 'title' in result
        assert 'genres' in result

    def test_movies_get_movies_by_genre_returns_sorted_list_of_ints(self):
        movies = Movies('../datasets/ml-latest-small/movies.csv')
        result = movies.get_movies_by_genre('Comedy')
        assert isinstance(result, list)
        assert all(isinstance(x, int) for x in result)
        assert result == sorted(result)

    def test_movies_get_genre_distribution_returns_sorted_tuples(self):
        movies = Movies('../datasets/ml-latest-small/movies.csv')
        result = movies.get_genre_distribution()
        assert isinstance(result, list)
        assert all(isinstance(x, tuple) and len(x) == 2 for x in result)
        assert all(isinstance(x[0], str) and isinstance(x[1], int) for x in result)
        # Проверка сортировки: по убыванию количества, затем по алфавиту
        for i in range(len(result) - 1):
            if result[i][1] == result[i+1][1]:
                assert result[i][0] <= result[i+1][0]
            else:
                assert result[i][1] >= result[i+1][1]

    def test_movies_get_all_movie_ids_returns_sorted_ints(self):
        movies = Movies('../datasets/ml-latest-small/movies.csv')
        result = movies.get_all_movie_ids()
        assert isinstance(result, list)
        assert all(isinstance(x, int) for x in result)
        assert result == sorted(result)

    def test_movies_get_movie_title_returns_string(self):
        movies = Movies('../datasets/ml-latest-small/movies.csv')
        result = movies.get_movie_title(1)
        assert isinstance(result, str)

    def test_movies_get_movies_count_returns_positive_int(self):
        movies = Movies('../datasets/ml-latest-small/movies.csv')
        result = movies.get_movies_count()
        assert isinstance(result, int)
        assert result > 0

    def test_movies_get_genres_list_returns_sorted_strings(self):
        movies = Movies('../datasets/ml-latest-small/movies.csv')
        result = movies.get_genres_list()
        assert isinstance(result, list)
        assert all(isinstance(x, str) for x in result)
        assert result == sorted(result)

    def test_movies_get_movie_info_raises_type_error_on_non_int(self):
        movies = Movies('../datasets/ml-latest-small/movies.csv')
        try:
            movies.get_movie_info("not_int")
            assert False, "Должно было возникнуть исключение TypeError"
        except TypeError:
            pass

    def test_movies_get_movie_info_raises_value_error_on_non_positive(self):
        movies = Movies('../datasets/ml-latest-small/movies.csv')
        try:
            movies.get_movie_info(-5)
            assert False, "Должно было возникнуть исключение ValueError"
        except ValueError:
            pass

    def test_movies_get_movies_by_genre_raises_type_error_on_non_str(self):
        movies = Movies('../datasets/ml-latest-small/movies.csv')
        try:
            movies.get_movies_by_genre(123)
            assert False, "Должно было возникнуть исключение TypeError"
        except TypeError:
            pass

    def test_movies_get_movies_by_genre_raises_value_error_on_empty_str(self):
        movies = Movies('../datasets/ml-latest-small/movies.csv')
        try:
            movies.get_movies_by_genre("")
            assert False, "Должно было возникнуть исключение ValueError"
        except ValueError:
            pass

    # Тесты для Ratings
    
    def test_ratings_get_user_ratings_returns_sorted_list(self):
        ratings = Ratings('../datasets/ml-latest-small/ratings.csv')
        result = ratings.get_user_ratings(1)
        assert isinstance(result, list)
        if result:
            assert all(isinstance(x, dict) for x in result)
            timestamps = [x['timestamp'] for x in result]
            assert timestamps == sorted(timestamps)

    def test_ratings_get_movie_ratings_returns_list_of_dicts(self):
        ratings = Ratings('../datasets/ml-latest-small/ratings.csv')
        result = ratings.get_movie_ratings(1)
        assert isinstance(result, list)
        assert all(isinstance(x, dict) for x in result)

    def test_ratings_get_top_rated_movies_returns_sorted_tuples(self):
        ratings = Ratings('../datasets/ml-latest-small/ratings.csv')
        result = ratings.get_top_rated_movies(5)
        assert isinstance(result, list)
        assert all(isinstance(x, tuple) and len(x) == 3 for x in result)
        assert all(isinstance(x[0], int) and isinstance(x[1], float) and isinstance(x[2], int) for x in result)
        avg_ratings = [x[1] for x in result]
        assert avg_ratings == sorted(avg_ratings, reverse=True)

    def test_ratings_get_rating_distribution_returns_sorted_by_rating(self):
        ratings = Ratings('../datasets/ml-latest-small/ratings.csv')
        result = ratings.get_rating_distribution()
        assert isinstance(result, list)
        assert all(isinstance(x, tuple) and len(x) == 2 for x in result)
        rating_vals = [x[0] for x in result]
        assert rating_vals == sorted(rating_vals)

    def test_ratings_get_average_user_rating_returns_float(self):
        ratings = Ratings('../datasets/ml-latest-small/ratings.csv')
        result = ratings.get_average_user_rating(1)
        assert isinstance(result, float)

    def test_ratings_get_ratings_count_returns_int(self):
        ratings = Ratings('../datasets/ml-latest-small/ratings.csv')
        result = ratings.get_ratings_count()
        assert isinstance(result, int)
        assert result >= 0

    def test_ratings_get_users_count_returns_int(self):
        ratings = Ratings('../datasets/ml-latest-small/ratings.csv')
        result = ratings.get_users_count()
        assert isinstance(result, int)
        assert result >= 0

    def test_ratings_methods_raise_value_error_on_invalid_id(self):
        ratings = Ratings('../datasets/ml-latest-small/ratings.csv')
        try:
            ratings.get_user_ratings(-1)
            assert False, "Должно было возникнуть исключение ValueError"
        except ValueError:
            pass
        try:
            ratings.get_movie_ratings("abc")
            assert False, "Должно было возникнуть исключение ValueError"
        except ValueError:
            pass

    # Тесты для Tags
    
    def test_tags_get_movie_tags_returns_sorted_strings(self):
        tags = Tags('../datasets/ml-latest-small/tags.csv')
        result = tags.get_movie_tags(1)
        assert isinstance(result, list)
        assert all(isinstance(x, str) for x in result)
        assert result == sorted(result)

    def test_tags_get_user_tags_returns_sorted_strings(self):
        tags = Tags('../datasets/ml-latest-small/tags.csv')
        result = tags.get_user_tags(1)
        assert isinstance(result, list)
        assert all(isinstance(x, str) for x in result)
        assert result == sorted(result)

    def test_tags_get_popular_tags_returns_sorted_tuples(self):
        tags = Tags('../datasets/ml-latest-small/tags.csv')
        result = tags.get_popular_tags(5)
        assert isinstance(result, list)
        assert all(isinstance(x, tuple) and len(x) == 2 for x in result)
        assert all(isinstance(x[0], str) and isinstance(x[1], int) for x in result)
        counts = [x[1] for x in result]
        assert counts == sorted(counts, reverse=True)

    def test_tags_get_all_tags_count_returns_int(self):
        tags = Tags('../datasets/ml-latest-small/tags.csv')
        result = tags.get_all_tags_count()
        assert isinstance(result, int)
        assert result >= 0

    def test_tags_get_unique_tags_count_returns_int(self):
        tags = Tags('../datasets/ml-latest-small/tags.csv')
        result = tags.get_unique_tags_count()
        assert isinstance(result, int)
        assert result >= 0

    def test_tags_methods_raise_value_error_on_invalid_id(self):
        tags = Tags('../datasets/ml-latest-small/tags.csv')
        try:
            tags.get_movie_tags(-5)
            assert False, "Должно было возникнуть исключение ValueError"
        except ValueError:
            pass

    # Тесты для Links
    
    def test_links_get_imdb_id_returns_int(self):
        links = Links('../datasets/ml-latest-small/links.csv')
        result = links.get_imdb_id(1)
        assert isinstance(result, int)

    def test_links_get_tmdb_id_returns_int(self):
        links = Links('../datasets/ml-latest-small/links.csv')
        result = links.get_tmdb_id(1)
        assert isinstance(result, int)

    def test_links_get_all_linked_movies_returns_sorted_ints(self):
        links = Links('../datasets/ml-latest-small/links.csv')
        result = links.get_all_linked_movies()
        assert isinstance(result, list)
        assert all(isinstance(x, int) for x in result)
        assert result == sorted(result)

    def test_links_get_links_count_returns_int(self):
        links = Links('../datasets/ml-latest-small/links.csv')
        result = links.get_links_count()
        assert isinstance(result, int)
        assert result >= 0

    def test_links_methods_raise_value_error_on_invalid_id(self):
        links = Links('../datasets/ml-latest-small/links.csv')
        try:
            links.get_imdb_id("invalid")
            assert False, "Должно было возникнуть исключение ValueError"
        except ValueError:
            pass