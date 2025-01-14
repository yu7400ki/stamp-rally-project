from collections import OrderedDict

from .models import Stamp
from django.shortcuts import render
from django.views.generic import TemplateView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin

# 各地のQRが持つURL
# https://ドメイン/stamp/get/UUID/

# パンフレットに載せるQRが持つURL
# https://ドメイン/stamp/ もしくは https://ドメイン/login/

# 各協賛のUUID
# query_lst[0] = アピレ
# query_lst[1] = イトーヨーカドー
# query_lst[2] = Beans
# query_lst[3] = ビビオ
# query_lst[4] = キャンパス
# query_lst = ["90400d45-8c8f-45d2-b384-d0f58f1b8f67",
#              "cf46968e-247d-4148-93c9-7b0e8518efcc",
#              "5bb08df7-8ac1-4cc9-a039-a9a9cbdfadca",
#              "d44658d9-cc4c-4025-a6d6-c3c90ac45a6b",
#              "46e79bc5-d968-465d-92bb-4b721f715d92",]

query_dict = OrderedDict()
query_dict["90400d45-8c8f-45d2-b384-d0f58f1b8f67"] = "アピレ"
query_dict["cf46968e-247d-4148-93c9-7b0e8518efcc"] = "イトーヨーカドー"
query_dict["5bb08df7-8ac1-4cc9-a039-a9a9cbdfadca"] = "ビーンズ"
query_dict["d44658d9-cc4c-4025-a6d6-c3c90ac45a6b"] = "ビビオ"
query_dict["46e79bc5-d968-465d-92bb-4b721f715d92"] = "キャンパス"

class stamp(LoginRequiredMixin, TemplateView):
    template_name = "stamp/stamp.html"
    def get_context_data(self, **kwargs):

        # ユーザー情報取得
        try:
            user_info = Stamp.objects.get(user=self.request.user)

        # 初期設定
        except Stamp.DoesNotExist:
            Stamp.objects.create(user=self.request.user, stamps=[False,False,False,False,False,False])
            user_info = Stamp.objects.get(user=self.request.user)
            print("ユーザー情報を新規作成しました。")

        # htmlに渡すテンプレートの値
        # {{ user }} や {{ stamps }} で取得可能

        # {{ user }} は各ユーザーが持つ一意の文字列
        # {{ stamps }} はbool値のリスト
        # {{ stamps[0]~[4] が各地のスタンプ、stamps[5] は景品の獲得有無 }}

        context = super().get_context_data(**kwargs)
        context["user"] = user_info.user
        context["stamps"] = user_info.stamps

        # 景品の管理
        #query = self.request.GET.get("used")
        #if query=="true":
            #update_stamps = user_info.stamps
            #update_stamps[5] = True

            #user_info.stamps = update_stamps
            #user_info.save()

            #context["stamps"] = update_stamps

        return context

    def post(self,request,*args,**kwargs):
        password = request.POST['password']

        # ユーザー情報取得
        try:
            user_info = Stamp.objects.get(user=self.request.user)

        # 初期設定
        except Stamp.DoesNotExist:
            Stamp.objects.create(user=self.request.user, stamps=[False,False,False,False,False,False])
            user_info = Stamp.objects.get(user=self.request.user)
            print("ユーザー情報を新規作成しました。")

        if password=="banecan":
            update_stamps = user_info.stamps
            update_stamps[5] = True

            user_info.stamps = update_stamps
            user_info.save()

        return rd_index(request)

class stamp_get(LoginRequiredMixin, TemplateView):
    template_name = "stamp/stamp_get.html"
    def get_context_data(self, **kwargs):

        # ユーザー情報取得
        try:
            user_info = Stamp.objects.get(user=self.request.user)

        # 初期設定
        except Stamp.DoesNotExist:
            Stamp.objects.create(user=self.request.user, stamps=[False,False,False,False,False,False])
            user_info = Stamp.objects.get(user=self.request.user)
            print("ユーザー情報を新規作成しました。")

        # htmlに渡すテンプレートの値
        # {{ user }} や {{ stamped }} で取得可能

        # {{ user }} は各ユーザーが持つ一意の文字列
        # {{ stamped }} はスタンプが新たに押されたかどうかのbool値
            # 初回のみ演出ではない場合、無視してもらって大丈夫です。
        # {{ stamp_num }} は押されたスタンプの番号
            # デフォルト(押されていない場合)は-1を取ります。

        context = super().get_context_data(**kwargs)
        context["user"] = user_info.user
        context["stamped"] = False
        context["stamp_num"] = -1
        context["place_name"] = ""

        # スタンプ付与
        query = self.kwargs["sponser"]
        if query in query_dict:
            keys = list(query_dict.keys())
            index = keys.index(query)
            update_stamps = user_info.stamps
            if not update_stamps[index]:
                context["stamped"] = True
            update_stamps[index] = True
            context["stamp_num"] = index
            context["place_name"] = query_dict[query]

            user_info.stamps = update_stamps
            user_info.save()

        # デバッグ用
        if query == "reset":
            update_stamps = user_info.stamps
            update_stamps = [False,False,False,False,False,False]

            user_info.stamps = update_stamps
            user_info.save()

        # デバッグ用
        if query == "all":
            update_stamps = user_info.stamps
            update_stamps = [True,True,True,True,True,False]

            user_info.stamps = update_stamps
            user_info.save()

        # デバッグ用
        debug_lst = ["0", "1", "2", "3", "4"]
        if query in debug_lst:
            update_stamps = user_info.stamps
            if not update_stamps[debug_lst.index(query)]:
                context["stamped"] = True
            update_stamps[int(query)] = True
            context["stamp_num"] = debug_lst.index(query)

            user_info.stamps = update_stamps
            user_info.save()

        # デバッグ用
        if query == "print":
            print(context["user"])
            print(context["stamped"])
            print(user_info.stamps)

        return context

#class stamp_prize(LoginRequiredMixin, TemplateView):
    #template_name = "stamp/stamp_prize.html"
    #def get_context_data(self, **kwargs):

        # ユーザー情報取得
        #try:
            #user_info = Stamp.objects.get(user=self.request.user)

        # 初期設定
        #except Stamp.DoesNotExist:
            #Stamp.objects.create(user=self.request.user, stamps=[False,False,False,False,False,False])
            #user_info = Stamp.objects.get(user=self.request.user)
            #print("ユーザー情報を新規作成しました。")

        # htmlに渡すテンプレートの値
        # {{ user }} や {{ stamps }} で取得可能

        # {{ user }} は各ユーザーが持つ一意の文字列
        # {{ stamps }} はbool値のリスト
        # {{ stamps[0]~[4] が各地のスタンプ、stamps[5] は景品の獲得有無 }}

        #context = super().get_context_data(**kwargs)
        #context["user"] = user_info.user
        #context["stamps"] = user_info.stamps

        #return context

class stamp_map(LoginRequiredMixin, TemplateView):
    template_name = "stamp/stamp_map.html"

class redirect_stamp(RedirectView):
    url = "http://127.0.0.1:8000/stamp/"
rd_index = redirect_stamp.as_view()

# 500エラー確認用
from django.http import HttpResponseServerError
def my_test_500_view(request):
    # Return an "Internal Server Error" 500 response code.
    return HttpResponseServerError
