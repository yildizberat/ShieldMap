fetch('/graph-data')
  .then(res => res.json())
  .then(data => {
    const svg = d3.select("svg");
    const width = window.innerWidth;
    const height = window.innerHeight;

    const container = svg.append("g");

    const color = d3.scaleOrdinal([
      "#4e79a7", "#f28e2b", "#e15759", "#76b7b2",
      "#59a14f", "#edc948", "#b07aa1", "#ff9da7",
      "#9c755f", "#bab0ab"
    ]);

    svg.call(
      d3.zoom()
        .scaleExtent([0.2, 5])
        .on("zoom", (event) => {
          container.attr("transform", event.transform);
        })
    );

    const simulation = d3.forceSimulation(data.nodes)
      .force("link", d3.forceLink(data.links).id(d => d.id).distance(100))
      .force("charge", d3.forceManyBody().strength(-300))
      .force("center", d3.forceCenter(width / 2, height / 2));

    const link = container.append("g")
      .attr("stroke", "#999")
      .attr("stroke-opacity", 0.6)
      .selectAll("line")
      .data(data.links)
      .enter().append("line")
      .attr("stroke-width", 1.5);

    const node = container.append("g")
      .selectAll("circle")
      .data(data.nodes)
      .enter().append("a")
      .attr("xlink:href", d => `https://${d.id}`)
      .attr("target", "_blank")
      .append("circle")
      .attr("r", 8)
      .attr("fill", d => color(d.group))
      .style("cursor", "pointer")
      .call(drag(simulation))
      .on("mouseover", function (event, d) {
        d3.select(this).transition().duration(200).attr("r", 14);
      })
      .on("mouseout", function (event, d) {
        d3.select(this).transition().duration(200).attr("r", 8);
      });

    const label = container.append("g")
      .selectAll("text")
      .data(data.nodes)
      .enter().append("text")
      .text(d => d.id)
      .attr("dx", 12)
      .attr("dy", ".35em")
      .attr("font-size", "10px")
      .attr("fill", "#ffffff");

    node.on("click", (event, d) => {
      if (d.fx != null && d.fy != null) {
        d.fx = null;
        d.fy = null;
      } else {
        d.fx = d.x;
        d.fy = d.y;
      }
    });

    simulation.on("tick", () => {
      link
        .attr("x1", d => d.source.x)
        .attr("y1", d => d.source.y)
        .attr("x2", d => d.target.x)
        .attr("y2", d => d.target.y);

      container.selectAll("circle")
        .attr("cx", d => d.x)
        .attr("cy", d => d.y);

      label
        .attr("x", d => d.x)
        .attr("y", d => d.y);
    });

    function drag(simulation) {
      return d3.drag()
        .on("start", (event) => {
          if (!event.active) simulation.alphaTarget(0.3).restart();
          event.subject.fx = event.subject.x;
          event.subject.fy = event.subject.y;
        })
        .on("drag", (event) => {
          event.subject.fx = event.x;
          event.subject.fy = event.y;
        })
        .on("end", (event) => {
          if (!event.active) simulation.alphaTarget(0);
        });
    }
  });
