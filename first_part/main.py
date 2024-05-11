import redis
from redis_lru import RedisLRU

from models import Quote, Author

client = redis.StrictRedis(host="localhost", port=6379)
cache = RedisLRU(client)


@cache
def find_by_tag(tag):
    quotes = Quote.objects(tags__iregex=tag)
    result = [q.quote for q in quotes]
    return result

@cache
def find_by_author(author):
    authors = Author.objects(fullname__iregex=author)
    result = {}
    for aut in authors:
        quotes = Quote.objects(author=aut)
        result[aut.fullname] = [q.quote for q in quotes]
    return result


@cache
def find_by_tags(*tags):
    result = {}
    quotes = Quote.objects(tags__in=tags)
    for q in quotes:
        result.setdefault(q.author.fullname, []).append(q.quote)
    return result


if __name__ == "__main__":
    while True:
        user_input = input("Enter - [command]:[value] -> ")
        try:
            if user_input == "exit":
                break
            elif user_input.startswith("name:"):
                result = user_input.split(":")
                print(find_by_author(result[1]))
            elif user_input.startswith("tag:"):
                result = user_input.split(":")
                print(find_by_tag(result[1]))
            elif user_input.startswith('tags:'):
                result = user_input.split(":")
                tags = result[1].split(',')
                print(find_by_tags(*tags))
            else:
                print("Error input")
        except ValueError as err:
            print(f"Input error {err}")
