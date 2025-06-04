from ninja import NinjaAPI


def get_api():
    api = NinjaAPI(title='To4ka API', version='1.0.0')

    # api.add_router({path}, {router})

    return api


ninja_api = get_api()
