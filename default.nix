{ pkgs ? import <nixpkgs> {} }:
with pkgs;
python3Packages.buildPythonApplication rec {
  pname = "&&NAME&&";
  version = "&&VERSION";
  src = ./.;
  propagatedBuildInputs = [];
  meta = {
    description = "&&DESCRIPTION&&";
  };
}
