filename_a = "bugfix_lines.txt"
filename_b = "unique.txt"

# ファイルBについて配列に格納
b_list = [] of String
File.open(filename_b) { |f_b|
    f_b.each_line { |b_line|
        b_list << b_line
    }
}

b_uniq = b_list.uniq # 重複を除く

cnt = 0
File.open("cmp_res.txt", "w") do |f|
  File.open(filename_a) { |f_a|
    f_a.each_line { |a_line|
        if b_uniq.includes?(a_line)
            f.puts(a_line)
        end
        cnt += 1
        if cnt % 1000 == 0
            p cnt
        end
    }
  }
end
