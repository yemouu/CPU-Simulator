{ pkgs, lib }:
pkgs.python3Packages.buildPythonApplication {
  pname = "CPU-Schedulers";
  version = "0.0.1";
  pyproject = true;

  src = ../../.;

  build-system = with pkgs.python3Packages; [ hatchling ];
  # dependencies = with pkgs.python3Packages; [ ];
  # nativeCheckInputs = [ ];

  meta = {
    description = "CPU Scheduler GUI to Compare CPU Schedulers";
    homepage = "https://github.com/yemouu/CPU-Simulator-GUI";
    license = lib.licenses.mit;
  };
}
