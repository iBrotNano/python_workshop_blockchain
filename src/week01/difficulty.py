ts_start_block = 1746306013
ts_end_block = 1747490339
duration = ts_end_block - ts_start_block
print(f"duration:               {duration} secs")

epoch_expected = 2016 * 10 * 60
print(f"expected epoch time:    {epoch_expected} secs")
difference = duration - epoch_expected
print(f"difference:             {difference} secs")

adjust = duration / epoch_expected
print(f"adjustment:             {adjust}")

max_target = int("00000000ffff0000000000000000000000000000000000000000000000000000", 16)
print(f"max_target:             {max_target}")

prev_target = int(
    "000000000000000000025ced0000000000000000000000000000000000000000", 16
)

print(f"prev_target:            {prev_target}")

new_target = int(prev_target * adjust)
print(f"new_target_hex:         0x{new_target:064x}")
print(f"new_target:             {new_target}")


new_difficulty = int(max_target / new_target)
print(f"new_difficulty:         {new_difficulty}")

min_difficulty = int(max_target / max_target)
print(f"min_difficulty:         {min_difficulty} @ genesis")

true_dfficulty = 121658450774825
print(f"true_dfficulty:         {true_dfficulty}")
ddiffer = int(true_dfficulty - new_difficulty)
print(f"ddiffer:                {ddiffer}")
inaccuracy = ddiffer / true_dfficulty * 100
print(f"inaccuracy:             {inaccuracy:.8f}%")
accuracy = 100 - inaccuracy
print(f"accuracy:               {accuracy:.8f}%")
