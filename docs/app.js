async function main() {
  const res = await fetch("./data/latest.json", { cache: "no-store" });
  const data = await res.json();

  document.getElementById("meta").textContent =
    `대상 날짜(KST): ${data.date_kst} · 생성 시각: ${data.generated_at_kst}`;

  const list = document.getElementById("list");
  list.innerHTML = "";

  (data.clusters || []).forEach((c, idx) => {
    const card = document.createElement("section");
    card.className = "card";

    const h2 = document.createElement("h2");
    h2.textContent = `${idx + 1}. ${c.rep_title}`;
    card.appendChild(h2);

    const small = document.createElement("div");
    small.className = "small";
    small.textContent = `유사 기사: ${c.items?.length || 0}개`;
    card.appendChild(small);

    const ul = document.createElement("ul");
    (c.items || []).slice(0, 6).forEach(it => {
      const li = document.createElement("li");
      li.innerHTML = `<a href="${it.link}" target="_blank" rel="noopener">${it.title}</a>
                      <span class="src">(${it.source})</span>`;
      ul.appendChild(li);
    });
    card.appendChild(ul);

    list.appendChild(card);
  });
}

main();