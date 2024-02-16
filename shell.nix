{ pkgs ? import <nixpkgs> {} }:
let my-python = pkgs.python3.withPackages (ps: with ps; [
    sortedcontainers
    flask
    pyautogui
  ]);
in my-python.env
