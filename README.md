# Code for CaST: Channel emulation generator and Sounder Toolchain
This repository contains the code for the paper D. Villa, M. Tehrani-Moayyed, P. Johari, S. Basagni, T. Melodia, "CaST: A Toolchain for Creating and Characterizing Realistic Wireless Network Emulation Scenarios," Proceedings of the 16th ACM Workshop on Wireless Network Testbeds, Experimental Evaluation &amp; CHaracterization (WiNTECH), October 2022.

This work was partially supported by the U.S. National Science Foundation under grant CNS-1925601, and U.S. Department of Transportation, Federal Highway Administration under grant 693JJ321C000009.

# How to use it

The channel sounding code of CaST has been adjusted to work on the Colosseum testbed. Colosseum users can make a reservation with the common image "cast" which already contains all latest code ready to run.

To run CaST channel sounding, users can simply leverage the step-by-step interactive bash script that will guide them to input all needed configurations and requirements by executing first on the tx node:
  ```
  ./cast_tx.sh
  ```
and then running the receiver node, which is going to perform also the cast post-processing operations, with:
  ```
  ./cast_rx.sh
  ```
It is recommended the use of terminal multiplexers like `tmux` or `screen`.

# References

[1] D. Villa, M. Tehrani-Moayyed, P. Johari, S. Basagni, T. Melodia, "CaST: A Toolchain for Creating and Characterizing Realistic Wireless Network Emulation Scenarios", Proc. of the 16th ACM Workshop on Wireless Network Testbeds, Experimental evaluation & CHaracterization (WiNTECH 2022), Sydney, Australia, October 2022. [[Paper]](https://ece.northeastern.edu/wineslab/papers/villa2022wintech.pdf)

[2] D. Villa, M. Tehrani-Moayyed, C. Robinson, L. Bonati, P. Johari, M. Polese, S. Basagni, T. Melodia, "Colosseum as a Digital Twin: Bridging Real-World Experimentation and Wireless Network Emulation," arXiv:2303.17063 [cs.NI], pp. 1-15, March 2023. [[Paper]](https://arxiv.org/pdf/2303.17063.pdf)

[3] L. Bonati, P. Johari, M. Polese, S. D'Oro, S. Mohanti, M. Tehrani-Moayyed, D. Villa, S. Shrivastava, C. Tassie, K. Yoder, A. Bagga, P. Patel, V. Petkov, M. Seltser, F. Restuccia, A. Gosain, K.R. Chowdhury, S. Basagni, T. Melodia, "Colosseum: Large-Scale Wireless Experimentation Through Hardware-in-the-Loop Network Emulation," Proc. of IEEE Intl. Symp. on Dynamic Spectrum Access Networks (DySPAN), Virtual Conference, December 2021. [[Paper]](https://ece.northeastern.edu/wineslab/papers/bonati2021colosseum.pdf)

[4] https://www.northeastern.edu/colosseum/

[5] https://www.github.com/wineslab/cast/