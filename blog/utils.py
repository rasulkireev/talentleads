from libgravatar import Gravatar


def get_garavatar_url(email):
    g = Gravatar(email)
    return g.get_image()
