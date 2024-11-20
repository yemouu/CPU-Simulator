{
  description = "CPU Scheduler GUI to Compare CPU Schedulers";

  inputs.nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";

  outputs = { self, nixpkgs }:
    let
      forAllSystems = function: nixpkgs.lib.genAttrs [ "x86_64-linux" ]
        (system: function (import nixpkgs {
          inherit system;
          overlays = [ self.overlays.default ];
        }));
    in
    {
      formatter = forAllSystems (pkgs: pkgs.nixpkgs-fmt);

      devShells = forAllSystems (pkgs: {
        default = pkgs.mkShell {
          buildInputs = with pkgs; [
            hatch
            mypy
            (python3.withPackages (py-pkgs: with py-pkgs; [
              build
              hatchling
            ]))
            ruff
          ];
        };
      });

      overlays.default = final: prev: {
        cpu-schedulers = final.callPackage ./nix/packages { };
      };

      packages = forAllSystems (pkgs: rec {
        default = cpu-schedulers;
        cpu-schedulers = pkgs.cpu-schedulers;
      });

      apps = forAllSystems (pkgs: rec {
        default = cpu-schedulers;
        cpu-schedulers = {
          type = "app";
          program = "${pkgs.cpu-schedulers}/bin/cpu-schedulers";
        };
      });
    };
}
