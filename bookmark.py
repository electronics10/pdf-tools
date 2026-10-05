from pypdf import PdfReader, PdfWriter
import pdfplumber
import re

# Extract the TOC text from the PDF and parse it to get the structure of bookmarks. Use split.py and ChatGPT to help with this.
# Manually create a nested structure of bookmarks based on the TOC.
TOC_PAGE = 10 # actual page number of the TOC, roman numeral page number, no offset
PREFACCE_PAGE = 7 # actual page number of the preface, roman numeral page number, no offset

OFFSET = 13 # if TOC page numbers are off by a constant amount, set it here
STRUCTURE = [
    ("1 Inverse Problems and Interpretation of Measurements", 1, [
        ("1.1 Introductory Examples", 3),
        ("1.2 Inverse Crimes", 5),
    ]),
    ("2 Classical Regularization Methods", 7, [
        ("2.1 Introduction: Fredholm Equation", 7),
        ("2.2 Truncated Singular Value Decomposition", 10),
        ("2.3 Tikhonov Regularization", 16),
        ("2.3.1 Generalizations of the Tikhonov Regularization", 24),
        ("2.4 Regularization by Truncated Iterative Methods", 27),
        ("2.4.1 Landweber-Fridman Iteration", 27),
        ("2.4.2 Kaczmarz Iteration and ART", 31),
        ("2.4.3 Krylov Subspace Methods", 39),
        ("2.5 Notes and Comments", 46),
    ]),
    ("3 Statistical Inversion Theory", 49, [
        ("3.1 Inverse Problems and Bayes' Formula", 50),
        ("3.1.1 Estimators", 52),
        ("3.2 Construction of the Likelihood Function", 55),
        ("3.2.1 Additive Noise", 56),
        ("3.2.2 Other Explicit Noise Models", 58),
        ("3.2.3 Counting Process Data", 60),
        ("3.3 Prior Models", 62),
        ("3.3.1 Gaussian Priors", 62),
        ("3.3.2 Impulse Prior Densities", 62),
        ("3.3.3 Discontinuities", 65),
        ("3.3.4 Markov Random Fields", 66),
        ("3.3.5 Sample-based Densities", 70),
        ("3.4 Gaussian Densities", 72),
        ("3.4.1 Gaussian Smoothness Priors", 79),
        ("3.5 Interpreting the Posterior Distribution", 90),
        ("3.6 Markov Chain Monte Carlo Methods", 91),
        ("3.6.1 The Basic Idea", 91),
        ("3.6.2 Metropolis-Hastings Construction of the Kernel", 94),
        ("3.6.3 Gibbs Sampler", 98),
        ("3.6.4 Convergence", 106),
        ("3.7 Hierarchical Models", 108),
        ("3.8 Notes and Comments", 112),
    ]),
    ("4 Nonstationary Inverse Problems", 115, [
        ("4.1 Bayesian Filtering", 115),
        ("4.1.1 A Nonstationary Inverse Problem", 116),
        ("4.1.2 Evolution and Observation Models", 118),
        ("4.2 Kalman Filters", 123),
        ("4.2.1 Linear Gaussian Problems", 123),
        ("4.2.2 Extended Kalman Filters", 126),
        ("4.3 Particle Filters", 129),
        ("4.4 Spatial Priors", 133),
        ("4.5 Fixed-lag and Fixed-interval Smoothing", 138),
        ("4.6 Higher-order Markov Models", 140),
        ("4.7 Notes and Comments", 143),
    ]),
    ("5 Classical Methods Revisited", 145, [
        ("5.1 Estimation Theory", 146),
        ("5.1.1 Maximum Likelihood Estimation", 146),
        ("5.1.2 Estimators Induced by Bayes Costs", 147),
        ("5.1.3 Estimation Error with Affine Estimators", 149),
        ("5.2 Test Cases", 150),
        ("5.2.1 Prior Distributions", 150),
        ("5.2.2 Observation Operators", 152),
        ("5.2.3 The Additive Noise Models", 155),
        ("5.2.4 Test Problems", 157),
        ("5.3 Sample-Based Error Analysis", 158),
        ("5.4 Truncated Singular Value Decomposition", 159),
        ("5.5 Conjugate Gradient Iteration", 162),
        ("5.6 Tikhonov Regularization", 164),
        ("5.6.1 Prior Structure and Regularization Level", 166),
        ("5.6.2 Misspecification of the Gaussian Observation Error Model", 170),
        ("5.6.3 Additive Cauchy Errors", 173),
        ("5.7 Discretization and Prior Models", 175),
        ("5.8 Statistical Model Reduction, Approximation Errors and Inverse Crimes", 181),
        ("5.8.1 An Example: Full Angle Tomography and CGNE", 184),
        ("5.9 Notes and Comments", 186),
    ]),
    ("6 Model Problems", 189, [
        ("6.1 X-ray Tomography", 189),
        ("6.1.1 Radon Transform", 190),
        ("6.1.2 Discrete Model", 192),
        ("6.2 Inverse Source Problems", 194),
        ("6.2.1 Quasi-static Maxwell's Equations", 194),
        ("6.2.2 Electric Inverse Source Problems", 197),
        ("6.2.3 Magnetic Inverse Source Problems", 198),
        ("6.3 Impedance Tomography", 202),
        ("6.4 Optical Tomography", 208),
        ("6.4.1 The Radiation Transfer Equation", 208),
        ("6.4.2 Diffusion Approximation", 211),
        ("6.4.3 Time-harmonic Measurement", 219),
        ("6.5 Notes and Comments", 219),
    ]),
    ("7 Case Studies", 223, [
        ("7.1 Image Deblurring and Recovery of Anomalies", 223),
        ("7.1.1 The Model Problem", 223),
        ("7.1.2 Reduced and Approximation Error Models", 225),
        ("7.1.3 Sampling the Posterior Distribution", 229),
        ("7.1.4 Effects of Modelling Errors", 234),
        ("7.2 Limited Angle Tomography: Dental X-ray Imaging", 236),
        ("7.2.1 The Layer Estimation", 239),
        ("7.2.2 MAP Estimates", 240),
        ("7.2.3 Sampling: Gibbs Sampler", 241),
        ("7.3 Biomagnetic Inverse Problem: Source Localization", 242),
        ("7.3.1 Reconstruction with Gaussian White Noise Prior Model", 243),
        ("7.3.2 Reconstruction of Dipole Strengths with the l1-prior Model", 245),
        ("7.4 Dynamic MEG by Bayes Filtering", 249),
        ("7.4.1 A Single Dipole Model", 250),
        ("7.4.2 More Realistic Geometry", 253),
        ("7.4.3 Multiple Dipole Models", 254),
        ("7.5 Electrical Impedance Tomography: Optimal Current Patterns", 260),
        ("7.5.1 A Posteriori Synthesized Current Patterns", 260),
        ("7.5.2 Optimization Criterion", 262),
        ("7.5.3 Numerical Examples", 265),
        ("7.6 Electrical Impedance Tomography: Handling Approximation Errors", 269),
        ("7.6.1 Meshes and Projectors", 270),
        ("7.6.2 The Prior Distribution and the Prior Model", 272),
        ("7.6.3 The Enhanced Error Model", 273),
        ("7.6.4 The MAP Estimates", 275),
        ("7.7 Electrical Impedance Process Tomography", 278),
        ("7.7.1 The Evolution Model", 280),
        ("7.7.2 The Observation Model and the Computational Scheme", 283),
        ("7.7.3 The Fixed-lag State Estimate", 285),
        ("7.7.4 Estimation of the Flow Profile", 286),
        ("7.8 Optical Tomography in Anisotropic Media", 291),
        ("7.8.1 The Anisotropy Model", 292),
        ("7.8.2 Linearized Model", 296),
        ("7.9 Optical Tomography: Boundary Recovery", 299),
        ("7.9.1 The General Elliptic Case", 300),
        ("7.9.2 Application to Optical Diffusion Tomography", 303),
        ("7.10 Notes and Comments", 305),
    ]),
    ("A Appendix: Linear Algebra and Functional Analysis", 311, [
        ("A.1 Linear Algebra", 311),
        ("A.2 Functional Analysis", 314),
        ("A.3 Sobolev Spaces", 316),
    ]),
    ("B Appendix 2: Basics on Probability", 319, [
        ("B.1 Basic Concepts", 319),
        ("B.2 Conditional Probabilities", 323),
    ]),
    ("References", 329),
    ("Index", 337),
]


# Seems to work better than trying to parse the TOC text.
def add_nested_bookmarks(input_pdf, output_pdf, structure):
    """
    structure: list of (title, page, [children]) tuples
    """
    reader = PdfReader(input_pdf)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)

    def add_items(items, parent=None):
        for item in items:
            title, page = item[0], item[1]
            children = item[2] if len(item) > 2 else []
            ref = writer.add_outline_item(title, page - 1 + OFFSET, parent=parent)
            if children:
                add_items(children, parent=ref)

    # Edge case: add top-level bookmarks for TOC and Preface if they are not included in the structure.
    if TOC_PAGE < PREFACCE_PAGE:
        ref = writer.add_outline_item("Contents", TOC_PAGE - 1)
        ref = writer.add_outline_item("Preface", PREFACCE_PAGE - 1)
    else:
        ref = writer.add_outline_item("Preface", PREFACCE_PAGE - 1)
        ref = writer.add_outline_item("Contents", TOC_PAGE - 1)
    add_items(structure)
    with open(output_pdf, "wb") as f:
        writer.write(f)


if __name__ == "__main__":
    add_nested_bookmarks("textbook.pdf", "textbook_bookmarked.pdf", STRUCTURE)
