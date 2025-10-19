import ijson
import math

file_path = "mesh_export.json"

X_min = Y_min = Z_min = math.inf
X_max = Y_max = Z_max = -math.inf

buffer = []

with open(file_path, "r", encoding="utf-8") as f:
    numbers = ijson.items(f, "objects.item.wires.item.item.item")  # cada número

    for num in numbers:
        buffer.append(float(num))  # converte decimal.Decimal para float
        if len(buffer) == 3:
            x, y, z = buffer
            X_min = min(X_min, x)
            X_max = max(X_max, x)
            Y_min = min(Y_min, y)
            Y_max = max(Y_max, y)
            Z_min = min(Z_min, z)
            Z_max = max(Z_max, z)
            buffer.clear()  # reinicia buffer para próximo vértice

print("Dimensões totais (bounding box):")
print(f"Width (X): {X_max - X_min}")
print(f"Depth (Y): {Y_max - Y_min}")
print(f"Height (Z): {Z_max - Z_min}")
