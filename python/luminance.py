import argparse
import csv
import json
import math

from utils.color_utils import relativeLuminance, color2hex, colors, colors_dic, rgb2hex

args = None


def checkWcagCompliance(contrast):
    if (contrast >= 7):
        return "AAA"
    elif (contrast >= 4.5):
        return "AA"
    else:
        return "None"


def calculateContrast(color1, color2):
    if (isinstance(color1, str)):
        color1 = colors_dic[color1]
    if (isinstance(color2, str)):
        color2 = colors_dic[color2]

    luminance1 = relativeLuminance(*color1)
    luminance2 = relativeLuminance(*color2)
    contrast = (max(luminance1, luminance2) + 0.05) / \
        (min(luminance1, luminance2) + 0.05)

    return contrast


def testColors(backgroundColors, foregroundColors):
    results = []
    for i in range(0, len(backgroundColors)):
        color = backgroundColors[i]
        bestColor = None
        contrast = None
        # test with all foreground colors
        for j in range(0, len(foregroundColors)):
            foregroundColor = foregroundColors[j]
            contrast = calculateContrast(color, foregroundColor)
            if (args.verbose):
                print("Testing color " + str(
                    rgb2hex(color)) + " with color " + str(color2hex(foregroundColor)) +
                    " (" + str(contrast) + ")")

            if (bestColor == None or contrast > bestContrast):
                bestColor = foregroundColor
                bestContrast = contrast

        compliance = checkWcagCompliance(bestContrast)
        results.append({"color": color, "bestColor": bestColor,
                       "contrast": bestContrast, "compliance": compliance})
    return results


def main(colorsToTest, increment):
    # create array of all colors
    colors = []
    for r in range(0, 256, increment):
        for g in range(0, 256, increment):
            for b in range(0, 256, increment):
                colors.append([r, g, b])

    results = testColors(colors, colorsToTest)
    rapport = {}
    minContrast = 21
    maxContrast = 1
    numAAA = 0
    numAA = 0
    testedColors = {}

    for result in results:
        if (result["contrast"] < minContrast):
            minContrast = result["contrast"]
        if (result["contrast"] > maxContrast):
            maxContrast = result["contrast"]

        if (result["compliance"] == "AAA"):
            numAAA += 1
        elif (result["compliance"] == "AA"):
            numAA += 1

        if (result["bestColor"] not in testedColors):
            testedColors[result["bestColor"]] = 1
        else:
            testedColors[result["bestColor"]] += 1

    if (args.verbose):
        print("Number of colors that are compliant with level AAA: " + str(numAAA))
        print("Number of colors that are compliant with level AA: " + str(numAA))
        print("Number of colors that are not compliant: " +
              str(len(results) - numAAA - numAA))
        print("Min contrast: " + str(minContrast))
        print("Max contrast: " + str(maxContrast))

    rapport["contrast"] = {"min": round(
        minContrast, 2), "max": round(maxContrast, 2)}
    rapport["compliance"] = {"AAA": numAAA, "AA": numAA,
                             "None": len(results) - numAAA - numAA}

    rapport["bestColors"] = {}
    for color in testedColors:
        if (args.verbose):
            print("Number of colors with " + str(color2hex(color)) +
                  " as best color: " + str(testedColors[color]))
        rapport["bestColors"][color2hex(color)] = testedColors[color]

    if (args.verbose):
        print("Number of colors tested: " +
              str(len(results)) + " / " + str(int(math.pow(256, 3))))
    rapport["colors"] = {"tested": len(
        results), "total": int(math.pow(256, 3))}

    writeResults(results)
    writeRapport(rapport)


def writeResults(results):
    with open(args.output + ".csv", 'w', newline='') as csvfile:
        fieldnames = ['color', 'bestColor', 'contrast', 'compliance']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            result["color"] = color2hex(result["color"])
            result["bestColor"] = color2hex(result["bestColor"])
            result["contrast"] = round(result["contrast"], 2)
            writer.writerow(result)


def writeRapport(rapport):
    with open(args.output + ".json", 'w') as jsonfile:
        json.dump(rapport, jsonfile, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--step", help="step",
                        type=int, default=8)
    parser.add_argument("-c", "--colors", help="color",
                        type=str, default="base")
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="store_true", default=False)
    parser.add_argument("-o", "--output", help="output file",
                        type=str, default="results")

    args = parser.parse_args()

    try:
        args.colors = colors[args.colors]
    except KeyError:
        print("Argument " + str(args.colors) + " is not valid")
        print("Valid arguments are: " + str(colors.keys()))
        exit()

    if (args.verbose):
        print("Running with colors " + str(args.colors) + " and step " +
              str(args.step), "will output to " + str(args.output))

    main(args.colors, args.step)
