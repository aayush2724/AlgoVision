"""/api/detect should recognise the classic algorithms whatever language the
student pastes them in (C, C++, Java, JavaScript/TypeScript, Python), and
spacing style (`a[j]>a[j+1]` vs `a[j] > a[j + 1]`) must not matter.
Unrelated code must still come back as `algorithm: null`."""
import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def detect(code):
    r = client.post("/api/detect", json={"code": code})
    assert r.status_code == 200
    return r.json()


POSITIVES = [
    # ── binary search ─────────────────────────────────────────────────
    ("binary_search", "cpp",
     "int search(vector<int>& a,int x){int l=0,r=a.size()-1;while(l<=r){int m=l+(r-l)/2;"
     "if(a[m]==x)return m;if(a[m]<x)l=m+1;else r=m-1;}return -1;}"),
    ("binary_search", "java",
     "public int find(int[] nums, int target) {\n  int left = 0, right = nums.length - 1;\n"
     "  while (left <= right) {\n    int mid = left + (right - left) / 2;\n"
     "    if (nums[mid] == target) return mid;\n    else if (nums[mid] < target) left = mid + 1;\n"
     "    else right = mid - 1;\n  }\n  return -1;\n}"),
    ("binary_search", "js",
     "function find(arr, t) {\n  let lo = 0, hi = arr.length - 1;\n  while (lo <= hi) {\n"
     "    const m = (lo + hi) >> 1;\n    if (arr[m] === t) return m;\n"
     "    if (arr[m] < t) lo = m + 1; else hi = m - 1;\n  }\n  return -1;\n}"),
    ("binary_search", "c",
     "int bs(int a[], int n, int k){ int low=0, high=n-1; while(low<=high){ int mid=(low+high)/2;"
     " if(a[mid]==k) return mid; else if(a[mid]<k) low=mid+1; else high=mid-1; } return -1; }"),
    # ── Kadane ────────────────────────────────────────────────────────
    ("kadanes", "java",
     "int maxSub(int[] a){int best=a[0],cur=0;for(int x:a){cur=Math.max(x,cur+x);"
     "best=Math.max(best,cur);}return best;}"),
    ("kadanes", "cpp",
     "int maxSubArray(vector<int>& nums) {\n  int sum = 0, ans = INT_MIN;\n  for (int x : nums) {\n"
     "    sum += x;\n    ans = max(ans, sum);\n    if (sum < 0) sum = 0;\n  }\n  return ans;\n}"),
    ("kadanes", "js",
     "function maxSub(a){ let cur = a[0], best = a[0];\n for (let i = 1; i < a.length; i++) {\n"
     "  cur = Math.max(a[i], cur + a[i]);\n  best = Math.max(best, cur);\n }\n return best; }"),
    ("kadanes", "python",
     "def f(a):\n  best=cur=a[0]\n  for x in a[1:]:\n    cur=max(x,cur+x); best=max(best,cur)\n  return best"),
    # ── simple sorts ──────────────────────────────────────────────────
    ("bubble_sort", "java",
     "void sort(int[] arr){int n=arr.length;for(int i=0;i<n-1;i++)for(int j=0;j<n-i-1;j++)"
     "if(arr[j]>arr[j+1]){int t=arr[j];arr[j]=arr[j+1];arr[j+1]=t;}}"),
    ("bubble_sort", "cpp",
     "void bsort(vector<int>& v){ for(size_t i=0;i<v.size();i++) for(size_t j=0;j+1<v.size()-i;j++)"
     " if(v[j]>v[j+1]) swap(v[j],v[j+1]); }"),
    ("bubble_sort", "js",
     "function sort(a){ for (let i = 0; i < a.length; i++) { for (let j = 0; j < a.length - 1 - i; j++) {"
     " if (a[j] > a[j + 1]) { [a[j], a[j + 1]] = [a[j + 1], a[j]]; } } } return a; }"),
    ("insertion_sort", "c",
     "void isort(int a[], int n){ for(int i=1;i<n;i++){ int key=a[i]; int j=i-1;"
     " while(j>=0 && a[j]>key){ a[j+1]=a[j]; j--; } a[j+1]=key; } }"),
    ("insertion_sort", "java",
     "static void sort(int[] arr) {\n for (int i = 1; i < arr.length; ++i) {\n  int key = arr[i];\n"
     "  int j = i - 1;\n  while (j >= 0 && arr[j] > key) {\n   arr[j + 1] = arr[j];\n   j = j - 1;\n  }\n"
     "  arr[j + 1] = key;\n }\n}"),
    ("selection_sort", "cpp",
     "void ssort(int a[], int n){ for(int i=0;i<n-1;i++){ int mn=i; for(int j=i+1;j<n;j++)"
     " if(a[j]<a[mn]) mn=j; swap(a[i],a[mn]); } }"),
    ("selection_sort", "js",
     "function sort(arr){ for(let i=0;i<arr.length;i++){ let minIdx=i;"
     " for(let j=i+1;j<arr.length;j++){ if(arr[j]<arr[minIdx]) minIdx=j; }"
     " [arr[i],arr[minIdx]]=[arr[minIdx],arr[i]]; } return arr; }"),
    # ── divide and conquer sorts ─────────────────────────────────────
    ("merge_sort", "cpp",
     "void merge(vector<int>& a,int l,int m,int r){vector<int> t; int i=l,j=m+1;"
     " while(i<=m&&j<=r) t.push_back(a[i]<=a[j]?a[i++]:a[j++]);"
     " while(i<=m) t.push_back(a[i++]); while(j<=r) t.push_back(a[j++]);"
     " for(int k=l;k<=r;k++) a[k]=t[k-l];}\n"
     "void sortArr(vector<int>& a,int l,int r){ if(l>=r) return; int m=l+(r-l)/2;"
     " sortArr(a,l,m); sortArr(a,m+1,r); merge(a,l,m,r);}"),
    ("quick_sort", "java",
     "int partition(int[] a, int lo, int hi) { int pivot = a[hi]; int i = lo - 1;"
     " for (int j = lo; j < hi; j++) if (a[j] < pivot) { i++; int t = a[i]; a[i] = a[j]; a[j] = t; }"
     " int t = a[i+1]; a[i+1] = a[hi]; a[hi] = t; return i + 1; }\n"
     "void sort(int[] a, int lo, int hi) { if (lo < hi) { int p = partition(a, lo, hi);"
     " sort(a, lo, p - 1); sort(a, p + 1, hi); } }"),
    # ── graphs ────────────────────────────────────────────────────────
    ("bfs", "cpp",
     "void traverse(int s, vector<vector<int>>& adj){ vector<bool> vis(adj.size()); queue<int> q;"
     " q.push(s); vis[s]=true; while(!q.empty()){ int u=q.front(); q.pop();"
     " for(int v: adj[u]) if(!vis[v]){ vis[v]=true; q.push(v);} } }"),
    ("bfs", "java",
     "void walk(int s, List<List<Integer>> adj) { boolean[] seen = new boolean[adj.size()];"
     " Queue<Integer> q = new ArrayDeque<>(); q.offer(s); seen[s] = true;"
     " while (!q.isEmpty()) { int u = q.poll(); for (int v : adj.get(u)) if (!seen[v]) { seen[v] = true; q.offer(v); } } }"),
    ("dfs", "cpp",
     "void go(int u, vector<vector<int>>& adj, vector<bool>& vis){ vis[u]=true;"
     " for(int v: adj[u]) if(!vis[v]) go(v, adj, vis); }"),
    ("dijkstra", "cpp",
     "vector<int> sp(int s, vector<vector<pair<int,int>>>& adj){ vector<int> dist(adj.size(), INT_MAX);"
     " priority_queue<pair<int,int>, vector<pair<int,int>>, greater<pair<int,int>>> pq;"
     " dist[s]=0; pq.push({0,s}); while(!pq.empty()){ auto [d,u]=pq.top(); pq.pop();"
     " for(auto [v,w]: adj[u]) if(dist[u]+w<dist[v]){ dist[v]=dist[u]+w; pq.push({dist[v],v}); } } return dist; }"),
    ("dijkstra", "java",
     "int[] sp(int src, List<int[]>[] g) { int[] dist = new int[g.length]; Arrays.fill(dist, Integer.MAX_VALUE);"
     " PriorityQueue<int[]> pq = new PriorityQueue<>((x, y) -> x[1] - y[1]); dist[src] = 0; pq.add(new int[]{src, 0});"
     " while (!pq.isEmpty()) { int[] cur = pq.poll(); for (int[] e : g[cur[0]])"
     " if (dist[cur[0]] + e[1] < dist[e[0]]) { dist[e[0]] = dist[cur[0]] + e[1]; pq.add(new int[]{e[0], dist[e[0]]}); } }"
     " return dist; }"),
    # ── array techniques ─────────────────────────────────────────────
    ("two_sum_sorted", "cpp",
     "bool has(vector<int>& a,int t){int i=0,j=a.size()-1;while(i<j){int s=a[i]+a[j];"
     "if(s==t)return true;if(s<t)i++;else j--;}return false;}"),
    ("two_sum_sorted", "js",
     "function pair(nums, target) { let left = 0, right = nums.length - 1;"
     " while (left < right) { const s = nums[left] + nums[right];"
     " if (s === target) return [left, right]; s < target ? left++ : right--; } return null; }"),
    ("sliding_window", "java",
     "int maxK(int[] a, int k){ int s=0; for(int i=0;i<k;i++) s+=a[i]; int best=s;"
     " for(int i=k;i<a.length;i++){ s+=a[i]-a[i-k]; best=Math.max(best,s);} return best; }"),
    ("dynamic_programming", "c",
     "int fib(int n){ if(n<=1) return n; return fib(n-1)+fib(n-2); }"),
    ("dynamic_programming", "java",
     "int climb(int n){ int[] dp = new int[n+1]; dp[0]=1; dp[1]=1;"
     " for(int i=2;i<=n;i++) dp[i]=dp[i-1]+dp[i-2]; return dp[n]; }"),
    # ── linked lists ─────────────────────────────────────────────────
    ("linked_list_reverse", "cpp",
     "Node* rev(Node* head){ Node* prev=nullptr; Node* cur=head;"
     " while(cur){ Node* nxt=cur->next; cur->next=prev; prev=cur; cur=nxt; } return prev; }"),
    ("linked_list_reverse", "java",
     "Node rev(Node head) { Node prev = null, curr = head; while (curr != null) {"
     " Node nxt = curr.next; curr.next = prev; prev = curr; curr = nxt; } return prev; }"),
    ("linked_list_reverse", "js",
     "function rev(head){ let prev = null; while (head) { const n = head.next;"
     " head.next = prev; prev = head; head = n; } return prev; }"),
    ("linked_list_reverse", "python",
     "def rev(head):\n  prev = None\n  while head:\n    nxt = head.next\n    head.next = prev\n"
     "    prev = head\n    head = nxt\n  return prev"),
]


@pytest.mark.parametrize("expected,lang,code", POSITIVES,
                         ids=[f"{e}-{lang}-{i}" for i, (e, lang, _) in enumerate(POSITIVES)])
def test_classic_is_recognised_in_any_language(expected, lang, code):
    body = detect(code)
    assert body["algorithm"] == expected, (lang, body["algorithm"], body["confidence"])
    assert body["confidence"] > 0
    assert body["realworld"] is not None


def test_spacing_style_does_not_change_the_score():
    tight = ("void s(int[] arr){for(int i=0;i<arr.length;i++)for(int j=0;j<arr.length-i-1;j++)"
             "if(arr[j]>arr[j+1]){int t=arr[j];arr[j]=arr[j+1];arr[j+1]=t;}}")
    loose = ("void s(int[] arr) { for (int i = 0; i < arr.length; i++) for (int j = 0; j < arr.length - i - 1; j++)"
             " if (arr[j] > arr[j + 1]) { int t = arr[j]; arr[j] = arr[j + 1]; arr[j + 1] = t; } }")
    a, b = detect(tight), detect(loose)
    assert a["algorithm"] == b["algorithm"] == "bubble_sort"
    assert a["confidence"] == b["confidence"]
    assert a["confidence"] >= 0.66


NEGATIVES = [
    ("c-hello", '#include <stdio.h>\nint main(void) {\n  printf("Hello, world!\\n");\n  return 0;\n}'),
    ("cpp-hello", '#include <iostream>\nusing namespace std;\nint main() {\n  cout << "Hello World" << endl;\n  return 0;\n}'),
    ("java-hello", 'public class Main {\n  public static void main(String[] args) {\n'
                   '    System.out.println("Hello, World!");\n  }\n}'),
    ("js-hello", 'console.log("Hello, world!");'),
    ("ts-hello", 'const greet = (name: string): string => `Hello, ${name}`;\nconsole.log(greet("world"));'),
    ("python-hello", 'print("Hello, world!")'),
    ("java-class", "public class Person {\n  private String name;\n  private int age;\n"
                   "  public Person(String name, int age) { this.name = name; this.age = age; }\n"
                   "  public String getName() { return name; }\n}"),
    ("js-class", "class Person {\n  constructor(name, age) { this.name = name; this.age = age; }\n"
                 "  greet() { return 'Hi ' + this.name; }\n}"),
    ("cpp-struct", "struct Point { int x, y; Point(int x, int y): x(x), y(y) {} };\n"
                   "int main(){ Point p(1,2); std::cout << p.x + p.y; }"),
    ("python-class", "class Dog:\n    def __init__(self, name):\n        self.name = name\n"
                     "    def speak(self):\n        return f'{self.name} says woof'"),
    ("c-sum", "int add(int a, int b) { return a + b; }"),
]


@pytest.mark.parametrize("label,code", NEGATIVES, ids=[n for n, _ in NEGATIVES])
def test_unrelated_code_is_not_misdetected(label, code):
    body = detect(code)
    assert body == {"algorithm": None, "confidence": 0.0, "realworld": None}, (label, body)
