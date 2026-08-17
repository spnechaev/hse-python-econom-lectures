#!/usr/bin/env ruby
# frozen_string_literal: true

# Split long Markdown cells at headings, without splitting fenced code blocks.

require "json"

def split_source(source)
  sections = []
  current = []
  in_fence = false

  source.each do |line|
    stripped = line.lstrip
    if !in_fence && stripped.match?(/^\#{1,6}\s/) && !current.empty?
      sections << current
      current = []
    end

    current << line
    in_fence = !in_fence if stripped.start_with?("```", "~~~")
  end

  sections << current unless current.empty?
  sections
end

ARGV.each do |filename|
  notebook = JSON.parse(File.read(filename, encoding: "UTF-8"))
  cells = notebook.fetch("cells")

  notebook["cells"] = cells.flat_map do |cell|
    next [cell] unless cell["cell_type"] == "markdown"

    sections = split_source(cell.fetch("source", []))
    next [cell] if sections.length == 1

    sections.each_with_index.map do |source, index|
      section = cell.dup
      section["source"] = source
      section["id"] = "#{cell.fetch("id", "markdown")}-#{index + 1}"
      section
    end
  end

  File.write(filename, JSON.pretty_generate(notebook) + "\n")
end
