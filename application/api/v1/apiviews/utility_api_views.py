from django.http import HttpResponse




from social_django.utils import psa
from social_core.backends.google import GoogleOAuth2
from rest_framework_simplejwt.tokens import RefreshToken


def register_by_access_token(request, backend):
    # This view expects an access_token GET parameter, if it's needed,
    # request.backend and request.strategy will be loaded with the current
    # backend and strategy.
    backend = GoogleOAuth2()
    # third_party_token = 'ya29.GltrB2iXmDGi05UfQR5_qSn7RtbGLgYZygrv8GCfn1sD2fwW4rVAhqsGfLsME9xzaB4BmGktx8IchkhEbIxeDDWLJbISRM1DoKO9qtEwZQ8_w6gSeVv6gVBH37hg'
    user = backend.do_auth(
        'ya29.GltrB_g6zAllGY9xmsO9gHxK5kTyRHyKtjlMJCRttOlUlOUh3F9BObtrmCXpQLIXXgt5uT85HNj_tZSm0Npt62g6L2JCqaFGDEtaFAhLydW7ZqxDxLnUqr2qeQPn')

    refresh = RefreshToken.for_user(user)
    print(str(refresh.access_token), '##################')
    print(user.__dict__, '**************')

    return HttpResponse('user found')





