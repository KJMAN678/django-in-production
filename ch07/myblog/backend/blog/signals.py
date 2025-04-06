from django import dispatch

# Signals を定義する
notify_author = dispatch.Signal()
