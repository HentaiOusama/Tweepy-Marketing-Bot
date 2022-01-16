<h1 align="center">Twitter Marketing Bot</h1>

## Information: -

There are three modes for this bot.
<ol type="1">
<li><code>Twitter API</code> : Uses twitter's API v1.1</li>
<li><code>Twitter Client</code> : Uses twitter's API v2.0</li>
<li><code>Manual Mode</code> : Uses selenium. It opens web browser and perform operation by finding HTML elements.</li>
</ol>

## Setup: -

Set up the following environment variables: -

(`R` => Required, `O` => Optional / Depend on actions, `NR` => Not Required)
<table border="1" align="center">
<tr>
<th align="center">Variable Name</th>
<th align="center">Value Format</th>
<th align="center">Twitter API</th>
<th align="center">Twitter Client</th>
<th align="center">Manual Mode</th>
</tr>
<tr>
<td><code>mode</code></td>
<td align="center"><code>int</code></td>
<td align="center">R &nbsp;&nbsp;( = 1)</td>
<td align="center">R &nbsp;&nbsp;( = 2)</td>
<td align="center">R &nbsp;&nbsp;( = 3)</td>
</tr>
<tr>
<td><code>twitterUsername</code></td>
<td align="center"><code>str</code></td>
<td align="center">NR</td>
<td align="center">NR</td>
<td align="center">R</td>
</tr>
<tr>
<td><code>twitterPassword</code></td>
<td align="center"><code>str</code></td>
<td align="center">NR</td>
<td align="center">NR</td>
<td align="center">R</td>
</tr>
<tr>
<td><code>consumer_key</code></td>
<td align="center"><code>str</code></td>
<td align="center">R</td>
<td align="center">R</td>
<td align="center">NR</td>
</tr>
<tr>
<td><code>consumer_key_secret</code></td>
<td align="center"><code>str</code></td>
<td align="center">R</td>
<td align="center">R</td>
<td align="center">NR</td>
</tr>
<tr>
<td><code>bearer_token</code></td>
<td align="center"><code>str</code></td>
<td align="center">R</td>
<td align="center">R</td>
<td align="center">NR</td>
</tr>
<tr>
<td><code>user_access_key</code></td>
<td align="center"><code>str</code></td>
<td align="center">O</td>
<td align="center">O</td>
<td align="center">NR</td>
</tr>
<tr>
<td><code>user_access_secret</code></td>
<td align="center"><code>str</code></td>
<td align="center">O</td>
<td align="center">O</td>
<td align="center">NR</td>
</tr>
<tr>
<td><code>mongo_username</code></td>
<td align="center"><code>str</code></td>
<td align="center">R</td>
<td align="center">R</td>
<td align="center">NR</td>
</tr>
<tr>
<td><code>mongo_password</code></td>
<td align="center"><code>str</code></td>
<td align="center">R</td>
<td align="center">R</td>
<td align="center">NR</td>
</tr>
<tr>
<td><code>mongo_cluster_name</code></td>
<td align="center"><code>str</code></td>
<td align="center">R</td>
<td align="center">R</td>
<td align="center">NR</td>
</tr>
<tr>
<td><code>mongo_database_name</code></td>
<td align="center"><code>str</code></td>
<td align="center">R</td>
<td align="center">R</td>
<td align="center">NR</td>
</tr>
<tr>
<td><code>threadsToRun</code></td>
<td align="center"><code>["int", ...]</code></td>
<td align="center">R</td>
<td align="center">R</td>
<td align="center">R</td>
</tr>
<tr>
<td><code>followUserId</code></td>
<td align="center"><code>int</code></td>
<td align="center">O</td>
<td align="center">O</td>
<td align="center">NR</td>
</tr>
<tr>
<td><code>foundThroughUserId</code></td>
<td align="center"><code>int</code></td>
<td align="center">O</td>
<td align="center">O</td>
<td align="center">NR</td>
</tr>
<tr>
<td><code>minFollowersCount</code></td>
<td align="center"><code>int</code></td>
<td align="center">O</td>
<td align="center">O</td>
<td align="center">O</td>
</tr>
<tr>
<td><code>maxFollowersCount</code></td>
<td align="center"><code>int</code></td>
<td align="center">O</td>
<td align="center">O</td>
<td align="center">O</td>
</tr>
<tr>
<td><code>minFollowingCount</code></td>
<td align="center"><code>int</code></td>
<td align="center">O</td>
<td align="center">O</td>
<td align="center">O</td>
</tr>
<tr>
<td><code>maxFollowingCount</code></td>
<td align="center"><code>int</code></td>
<td align="center">O</td>
<td align="center">O</td>
<td align="center">O</td>
</tr>
<tr>
<td><code>baseTagMessage</code></td>
<td align="center"><code>str</code></td>
<td align="center">O</td>
<td align="center">O</td>
<td align="center">O</td>
</tr>
</table>

If you plan to use the Manual Mode, you also need to perform the following steps: -
<ol type="1">
<li>Go to <a href="https://github.com/mozilla/geckodriver/releases">Geko Driver</a> and download the file that suits your PC.</li>
<li>Extract the downloaded file and paste the contents in <code>PROJECT_ROOT/venv</code></li>
<li>Set the <code>PATH</code> on your PC (Globally): - <code>PROJECT_ROOT/venv</code></li>
<li><code>(Optional)</code> You may find the path to default profile for mozilla and pass it as argument when creating object of <code>TwitterManualMode</code>. With this, you won't have to log in to twitter everytime you run the script.</li>
</ol>
(Note:- <code>PROJECT_ROOT</code> is the complete path to the directory where <code>main.py</code> file is located.)

## How to run: -

Run the main.py file using the command `python main.py` in the root directory.

## Purpose of Each Thread: -

<table border="1" align="center">
<tr>
<th align="center">Thread Number</th>
<th align="center">Twitter API</th>
<th align="center">Twitter Client</th>
<th align="center">Manual Mode</th>
</tr>
<tr>
<td align="center">1</td>
<td align="center">-</td>
<td align="center">Follow users stored in DB</td>
<td align="center">Follow users with <code>username</code> specified in <code>TwitterHelper/Input/ToFollowList.txt</code></td>
</tr>
<tr>
<td align="center">2</td>
<td align="center">-</td>
<td align="center">Fetch followers of <code>followUserId</code> and store in DB</td>
<td align="center">Tag users with <code>username</code> specified in <code>TwitterHelper/Input/ToTagList.txt</code> with <code>baseTagMessage</code></td>
</tr>
<tr>
<td align="center">3</td>
<td align="center">-</td>
<td align="center">Tag users stored in DB with <code>baseTagMessage</code></td>
<td align="center">-</td>
</tr>
</table>
