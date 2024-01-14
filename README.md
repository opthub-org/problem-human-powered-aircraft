# problem-human-powered-aircraft
## Benchmark Problem Definition
The benchmark problems are formulated as single or multi-objective minimization problems in the normalized design space:

$$
\begin{align*}
& \text{minimize}   & \quad & {\mathbf F({\mathbf x}_l)} = (f_1({\mathbf x}_l), \cdots, f_M({\mathbf x}_l)) \\
& \text{subject to} & \quad & {\mathbf G({\mathbf x}_l)} = (g_1({\mathbf x}_l), \cdots, g_N({\mathbf x}_l)) \leq 0 \\
&                   & \quad & {\mathbf x}_l \in [0, 1]^{D_l} \\
\end{align*}
$$

We classify problems as HPA $MNL$ − $l$, where $M$ is the number of objectives, $N$ is the number of constraints (excluding box constraints), $L$ is the problem index, and $l \in$ {0,1,2} is the difficulty level, which may be omitted if irrelevant. Higher $l$ indicates greater design variable freedom. 

The benchmark includes 60 problems (20 types $\times$ 3 levels) with 1-9 objectives. Original constrained problems (HPA \* $N$ \*) can also be used as unconstrained problems (HPA \* 0 \*) by means of a pre-implemented penalty method. The following table summarizes the design variable dimension $D_l$ at $n=4$ for each problem and difficulty level. Further details are in the original paper.

<p align="center">

| Problem      | $D_0$ | $D_1$ | $D_2$ |
|--------------|-------|-------|-------|
| HPA131, 101  | 17    | 32    | 108   |
| HPA142, 102  | 16    | 31    | 187   |
| HPA143, 103  | 18    | 33    | 189   |
| HPA241, 201  | 18    | 33    | 109   |
| HPA222, 202  | 16    | 31    | 187   |
| HPA233, 203  | 19    | 34    | 190   |
| HPA244, 204  | 18    | 33    | 189   |
| HPA245, 205  | 18    | 33    | 189   |
| HPA341, 301  | 18    | 33    | 109   |
| HPA322, 302  | 16    | 31    | 187   |
| HP333, A303  | 19    | 34    | 190   |
| HPA344, 304  | 18    | 33    | 189   |
| HPA345, 305  | 18    | 33    | 189   |
| HPA441, 401  | 18    | 33    | 189   |
| HPA422, 402  | 16    | 31    | 187   |
| HPA443, 403  | 18    | 33    | 189   |
| HPA541, 501  | 18    | 33    | 189   |
| HPA542, 502  | 19    | 34    | 190   |
| HPA641, 601  | 18    | 33    | 189   |
| HPA941, 901  | 19    | 34    | 190   |

</p>


## Build&Run

Build a docker image
```
docker build -t opthub/problem-real-world-optimization:latest .
```

Run the image with problem name as "PROBLEM=hpa201-1" for HPA201-1
```
docker run -it --rm -e PROBLEM=hpa201-1 opthub/problem-real-world-optimization:latest
```


## Input
The program reads one line of standard input and evaluates it as a single solution. The input is a JSON string as follows. "variable" is a list expressing ${\mathbf x}_l \in [0, 1]^{D_l}$

```
{"variable": [0.8,0.7,0.7,0.4,0.6,0.6,0.5,0.3,0,0,1,1,1,1,1,1,1,1,0.9,0.9,0.9,0.9,0.6,0.6,0.6,0.6,1,1,0.2,0.2,0.8,0.8,0.8]}
```


## Outut
The program writes the evaluation of one solution in the last line of the standard output


| key          | type                    | description                                          |
| ------------ | ----------------------- | ---------------------------------------------------- |
| `objective`  | `list[float]`           | objective function values. `null` if error.          |
| `constraint` | `list[float]` \| `null` | constraint function values. `null` if no constraint. |
| `error`      | `null`                  | not used.                                            |
| `info`       | `null`                  | not used.                                            |

## License
This project is under the BSD 3-Clause Clear License. See [LICENSE](LICENSE) for details.