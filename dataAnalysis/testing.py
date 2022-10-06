print("Get ready to import some shiz")
from traceroute_analysis import traceroute_analysis
from traceroute_collection import gap_detected

print("Alright, Im starting now...")
testing1, testing2 = gap_detected(
    "24.49.90.3.txt", 1662680942.4790363, 1662806033.300248, True
)
print("testing1:\n", testing1)
print("testing2:\n", testing2)
output = traceroute_analysis(testing1, testing2)
print("Output:", output)
