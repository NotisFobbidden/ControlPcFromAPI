{ pkgs ? import <nixpkgs> {} }:
let my-python = pkgs.python3.withPackages (ps: with ps; [
    sortedcontainers
    flask
    flask-cors
    pyautogui
  ]);
in my-python.env
