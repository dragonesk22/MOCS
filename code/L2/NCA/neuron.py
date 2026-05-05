#!/usr/bin/env python3
# created by Group Supermodels in VT2026
# for the course Modelling of Complex Systems at Uppsala University
# Group Members:
# Juan Rodriguez
# Björk Lucas
# Vootele Mets
# Marco Malosti
# Sofia Fernandes
# David Weingut

"""
 * This code is based on 
 *
 * gameOfLifeInteractiveToric.py
 *
 * which was given to us in the context of the Modelling Complex Systems Course 2026 at Uppsala University
 *
 * Copyright (c) 2026, Jordi-Lluis Figueras
 *
 * Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
 *
 * Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
 * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
 *
 * OpenAI Codex / ChatGPT 5.4 has been used in the editing of this file.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
"""

"""Neuron cellular automaton with periodic boundary conditions.

Usage:
  - Click on the grid once to produce a ready cell and twice for a firing cell
  - Press Run to start the evolution.
  - Press Pause to stop it.
  - Step advances one generation.
  - Clear resets the board.
  - Random fills the board with a random initial condition.
  
The board uses periodic boundary conditions, so gliders that leave one side of
the grid re-enter on the opposite side.
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch


nRows = 30
nCols = 30
updateIntervalMs = 100
rulesText = (
  "Neuron Cellular Automaton\n\n"
  "1. A ready neuron becomes firing at the next step if exactly two of its neighbours are firing.\n"
  "2. A firing neuron becomes resting at the next step.\n"
  "3. A resting neuron becomes ready at the next step.\n"
  "This version uses periodic boundary conditions. Cells leaving one edge "
  "re-enter through the opposite edge."
)


#new function to have three states
def count_neighbors_by_state(grid, state):
    return sum(
        np.roll(np.roll(grid == state, i, axis=0), j, axis=1)
        for i in (-1, 0, 1)
        for j in (-1, 0, 1)
        if not (i == 0 and j == 0)
    )

#list with ready and firing neighbours
def lifeStep(grid):
    n1 = count_neighbors_by_state(grid, 1)
    n2 = count_neighbors_by_state(grid, 2)

#implementation of the new rules
    new = np.zeros_like(grid)
    new[(grid==1) & (n2==2)] = 2
    new[(grid==2)] = 0
    new[(grid==0)] = 1
    new[(grid==1) & (n2!=2)] = 1

    return new


class GameOfLifeApp:
  def __init__(self):
    self.grid = np.ones((nRows, nCols), dtype = int)
    self.isRunning = False
    self.isMouseDown = False
    self.drawValue = 1
    self.rulesFigure = None

    self.fig = plt.figure(figsize = (12, 9))
    self.ax = self.fig.add_axes([0.05, 0.08, 0.70, 0.86])

    self.cmap = ListedColormap(["white", "black", "red"]) #colours used for the three states

    self.image = self.ax.imshow(
        self.grid,
        cmap=self.cmap,
        interpolation="nearest",
        vmin=0,
        vmax=2,
        origin="upper",
    )

    self.ax.set_title(f"Neuron Cellular Automaton (periodic {nRows} x {nCols} grid)", fontsize = 14)
    self.ax.set_xticks(np.arange(-0.5, nCols, 1), minor = True)
    self.ax.set_yticks(np.arange(-0.5, nRows, 1), minor = True)
    self.ax.grid(which = "minor", color = "lightgray", linewidth = 0.20)
    self.ax.tick_params(which = "both", bottom = False, left = False, labelbottom = False, labelleft = False)

    self.statusText = self.fig.text(
      0.05,
      0.02,
      "Click cells to toggle them. Periodic boundaries are active.",
      fontsize = 11,
    )

    self.timer = self.fig.canvas.new_timer(interval = updateIntervalMs)
    self.timer.add_callback(self.advanceOneStep)

    legendElements = [
    Patch(facecolor="white", edgecolor="black", label="Resting"),
    Patch(facecolor="black", edgecolor="black", label="Ready"),
    Patch(facecolor="red", edgecolor="black", label="Firing"),
    ]


    self.ax.legend(
      handles=legendElements,
      loc="upper left",
      bbox_to_anchor=(1.11, 0.5),
    )
    '''
    self.fig.text(0.80, 0.10,
    "States:\n0 = Resting\n1 = Ready\n2 = Firing",
    fontsize=10)
    '''
    self.runButton = self._makeButton([0.80, 0.82, 0.15, 0.055], "Run", self.toggleRun)
    self.stepButton = self._makeButton([0.80, 0.75, 0.15, 0.055], "Step", self.stepOnce)
    self.clearButton = self._makeButton([0.80, 0.68, 0.15, 0.055], "Clear", self.clearGrid)
    self.randomButton = self._makeButton([0.80, 0.61, 0.15, 0.055], "Random", self.randomizeGrid)
    self.rulesButton = self._makeButton([0.80, 0.54, 0.15, 0.055], "Rules", self.showRules)

    self.fig.canvas.mpl_connect("button_press_event", self.onMousePress)
    self.fig.canvas.mpl_connect("button_release_event", self.onMouseRelease)
    self.fig.canvas.mpl_connect("motion_notify_event", self.onMouseMove)
    self.fig.canvas.mpl_connect("close_event", self.onClose)

  def _makeButton(self, rect, label, callback):
    axis = self.fig.add_axes(rect)
    button = Button(axis, label)
    button.on_clicked(callback)
    return button

  def gridCoordinates(self, event):
    if event.inaxes != self.ax or event.xdata is None or event.ydata is None:
      return None

    col = int(np.floor(event.xdata + 0.5))
    row = int(np.floor(event.ydata + 0.5))

    if row < 0 or row >= nRows or col < 0 or col >= nCols:
      return None

    return row, col

  def refreshDisplay(self):
    self.image.set_data(self.grid)
    self.fig.canvas.draw_idle()

  def updateStatus(self, text):
    self.statusText.set_text(text)
    self.fig.canvas.draw_idle()

  def paintCell(self, row, col, value):
    if self.grid[row, col] != value:
      self.grid[row, col] = value
      self.refreshDisplay()
  '''
  def placePattern(self, pattern, anchorRow = None, anchorCol = None):
    if anchorRow is None:
      patternHeight = max(row for row, _ in pattern) + 1
      anchorRow = (nRows - patternHeight) // 2

    if anchorCol is None:
      patternWidth = max(col for _, col in pattern) + 1
      anchorCol = (nCols - patternWidth) // 2

    self.grid.fill(0)
    for rowOffset, colOffset in pattern:
      row = (anchorRow + rowOffset) % nRows
      col = (anchorCol + colOffset) % nCols
      self.grid[row, col] = 1
  
    self.refreshDisplay()
  
  def loadPreset(self, name):
    if self.isRunning:
      self.toggleRun(None)

    self.placePattern(presetPatterns[name])
    self.updateStatus(f"Loaded preset: {name}.")
  '''
  def onMousePress(self, event):
    coordinates = self.gridCoordinates(event)
    if coordinates is None:
      return

    row, col = coordinates
    self.isMouseDown = True
    self.drawValue = (self.grid[row, col] + 1) % 3
    self.paintCell(row, col, self.drawValue)

  def onMouseMove(self, event):
    if not self.isMouseDown:
      return

    coordinates = self.gridCoordinates(event)
    if coordinates is None:
      return

    row, col = coordinates
    self.paintCell(row, col, self.drawValue)

  def onMouseRelease(self, _event):
    self.isMouseDown = False

  def toggleRun(self, _event):
    if self.isRunning:
      self.isRunning = False
      self.timer.stop()
      self.runButton.label.set_text("Run")
      self.updateStatus("Simulation paused. You can keep editing the grid.")
    else:
      self.isRunning = True
      self.timer.start()
      self.runButton.label.set_text("Pause")
      self.updateStatus("Simulation running with periodic boundaries.")
      self.fig.canvas.draw_idle()

  def stepOnce(self, _event):
    if self.isRunning:
      self.toggleRun(None)

    self.advanceOneStep()
    self.updateStatus("Advanced one generation.")

  def clearGrid(self, _event):
    if self.isRunning:
      self.toggleRun(None)

    self.grid.fill(1)
    self.refreshDisplay()
    self.updateStatus("Grid cleared.")

  def randomizeGrid(self, _event):
    if self.isRunning:
      self.toggleRun(None)
    
    probs = [0.1, 0.8, 0.1]  # states 0,1,2
    self.grid = np.random.choice([0,1,2], size=(nRows,nCols), p=probs)

    
    self.refreshDisplay()
    self.updateStatus("Random initial condition loaded.")


  def showRules(self, _event):
    if self.rulesFigure is not None and plt.fignum_exists(self.rulesFigure.number):
      self.rulesFigure.canvas.manager.show()
      self.rulesFigure.canvas.draw_idle()
      return

    self.rulesFigure = plt.figure(figsize = (6.8, 4.0))
    self.rulesFigure.suptitle("Game of Life Rules", fontsize = 13)
    rulesAxis = self.rulesFigure.add_axes([0.06, 0.08, 0.88, 0.8])
    rulesAxis.axis("off")
    rulesAxis.text(0.0, 1.0, rulesText, va = "top", fontsize = 11, wrap = True)
    self.rulesFigure.canvas.draw_idle()

  def advanceOneStep(self):
    self.grid = lifeStep(self.grid)
    self.refreshDisplay()

  def onClose(self, _event):
    self.timer.stop()


def main():
  GameOfLifeApp()
  plt.show()


if __name__ == "__main__":
  main()
